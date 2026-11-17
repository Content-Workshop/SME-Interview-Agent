"""Core logic for the SME interview prototype: brands, prompts, Claude calls, storage.

Nothing here depends on Streamlit, so it can be tested on its own.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).parent
BRANDS_DIR = ROOT / "brands"
TEMPLATES_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output"

# Models the app offers, cheapest last. Costs are rough estimates per interview.
MODELS = {
    "claude-sonnet-5-5": "Sonnet 5.5 (~$0.50 to $1 per interview)",
    "claude-opus-5-5": "Opus 5.5 (~$1 to $2, sharpest follow-ups)",
    "claude-haiku-5-5": "Haiku 5.5 (a few cents, weaker follow-ups)",
}
DEFAULT_MODEL = "claude-sonnet-5-5"
# If the model declines a request, the API retries it on a fallback model.
# Haiku 5.5 has no server-side fallback, so it is sent without one.
FALLBACK_BETA = "server-side-fallback-2026-07-01"
NO_FALLBACK = {"claude-haiku-5-5"}

GENERIC = "generic"
FILE_START = "<<<INTERVIEW_FILE>>>"
FILE_END = "<<<END_INTERVIEW_FILE>>>"


# ---------------------------------------------------------------- brands


@dataclass
class Brand:
    slug: str
    name: str
    fields: dict[str, str]
    context: str  # brand.md, in full
    keywords: str
    posts: str  # existing-post index, or "" if none
    past_interviews: list[tuple[str, str]]  # (filename, text)


def list_brands() -> list[str]:
    return sorted(p.name for p in BRANDS_DIR.iterdir() if (p / "brand.md").is_file())


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def parse_fields(brand_md: str) -> dict[str, str]:
    """Read '- KEY: value' lines under '## Template fields'."""
    match = re.search(r"## Template fields\n(.*?)(?=\n## |\Z)", brand_md, re.S)
    if not match:
        return {}
    pairs = re.findall(r"^- ([A-Z_]+): (.+)$", match.group(1), re.M)
    return {key: value.strip() for key, value in pairs}


def load_brand(slug: str) -> Brand:
    folder = BRANDS_DIR / slug
    context = _read(folder / "brand.md")
    fields = parse_fields(context)
    past = [
        (p.name, _read(p)) for p in sorted((folder / "past-interviews").glob("*.md"))
    ]
    # Interviews completed in this app count as past interviews too.
    for done in sorted((OUTPUT_DIR / slug).glob("*/interview.md")):
        past.append((f"{done.parent.name}.md", _read(done)))
    return Brand(
        slug=slug,
        name=fields.get("BRAND_NAME", slug),
        fields=fields,
        context=context,
        keywords=_read(folder / "keywords.md"),
        posts=_read(folder / "posts.md"),
        past_interviews=past,
    )


# ------------------------------------------------------------- templates


@dataclass
class Setup:
    """What the person setting up the interview enters."""

    sme_name: str
    sme_role: str = ""
    sme_expertise: str = ""
    core_task: str = ""
    focus_topics: str = ""
    time_target: str = "20 to 30 minutes"
    quick_mode: bool = False


def prepare_generic(template: str, brand: Brand, setup: Setup) -> str:
    """Fill the generic template's placeholders and turn it into a READY interview.

    Does what Build Mode would: removes Part 1 and the "About This Template"
    section, and sets Template status to READY.
    """
    values = dict(brand.fields)
    values.update(
        SME_NAME=setup.sme_name,
        SME_ROLE=setup.sme_role or "subject-matter expert",
        SME_EXPERTISE=setup.sme_expertise or "see their answers",
        CORE_TASK=setup.core_task or "the core work they do",
        PRIORITY_TOPICS=setup.focus_topics or "none specified",
        TIME_TARGET=setup.time_target,
    )
    text = template
    text = re.sub(r"\n## About This Template\n.*?(?=\n# PART 2)", "\n", text, flags=re.S)
    text = re.sub(r"\n# PART 1: BUILD MODE\n.*?(?=\n# PART 2)", "\n", text, flags=re.S)
    text = text.replace("**Template status:** TEMPLATE", "**Template status:** READY")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def template_for(brand: Brand, setup: Setup) -> str:
    """Every interview uses the generic template, tailored to the brand and SME."""
    return prepare_generic(_read(TEMPLATES_DIR / "generic.md"), brand, setup)


# --------------------------------------------------------------- prompts

APP_RULES = f"""\
You are running an SME interview inside a prototype app. The interview file is
below. Follow its interviewer instructions exactly, with these app rules on top.
Where an app rule conflicts with the file, the app rule wins.

1. Interviewee. The first user message names the interviewee and gives setup
   details. Address them by that name, even if the file was written for
   someone else. Use they/them unless they tell you otherwise.

2. Use what's already known. You have the brand's context, its target
   keywords, its existing posts, and past interviews. Don't ask for anything
   these already answer. Don't summarize them to the interviewee.

3. Existing posts. When an answer overlaps a post in the existing-post index,
   use your one follow-up to ask how their view differs. Name the post by its
   title and say in one short clause what it argues, then ask what's different
   or new in their take. Don't do this for loose topical matches.

4. Focus topics. If the setup lists focus topics, lean the interview toward
   them: tailor question wording to them, and prefer questions where they fit.
   Don't force a topic into a question where it doesn't belong.

5. Tailoring. The file's questions are written generically. Never ask them
   as written. Before each question, rewrite it so it points at something
   specific: a focus topic, the SME's role or expertise, something they said
   in a past interview or earlier in this one, or a specific existing post.
   Test: if the question could be asked of anyone in the industry, rewrite
   it. Pointing at a past answer or a post is fine; suggesting what the SME
   should say is not. If setup gives focus topics, replace the generic
   warm-up (Q0.1) with an opening question that ties the first focus topic
   to something concrete from their past interviews or a recent post. Size
   the interview to the time target using the file's sizing table. Add optional modules that fit the brand's content
   goals. If the brand context defines extra flags (such as [ROADMAP] or
   [TEST]), apply them the same way as [ANON] and [CHECK], and list them in
   the wrap-up.

6. Quick mode. If quick mode is on (from setup or the `quick mode` command),
   ask a follow-up ONLY when an answer is under one sentence, or when it
   clearly overlaps an existing post (rule 3). Otherwise go straight to the
   next question.

7. Client names. Ask about anonymization once per name. Keep real names in
   the recorded file and add `[ANON]` right after each one the interviewee
   wants anonymized. The app removes them later from anything meant for
   publishing; the person receiving the interview sees the real names.

8. Saving. The app saves progress after every message. On `pause`, reply in
   one line that progress is saved and they can resume from the sidebar. On
   `resume`, carry on from the last unanswered question.

9. Finishing. When the interview ends (after the wrap-up, or on `finish`),
   send one short thank-you line, then the complete interview file with every
   answer recorded, between these exact markers on their own lines:
   {FILE_START}
   (the complete file in Markdown, not inside a code block)
   {FILE_END}
   Don't offer to run the AI Processing Instructions; the app has a button
   for that.

10. Keep messages short: one question at a time, a few words of transition.
"""


def _past_interviews_text(brand: Brand) -> str:
    if not brand.past_interviews:
        return "None yet."
    return "\n\n".join(f"### {name}\n\n{text}" for name, text in brand.past_interviews)


def context_blocks(brand: Brand) -> list[dict]:
    """Brand knowledge shared by the interview and the idea bank. Stable, so cacheable."""
    return [
        {"type": "text", "text": f"<brand_context>\n{brand.context}\n</brand_context>"},
        {"type": "text", "text": f"<target_keywords>\n{brand.keywords}\n</target_keywords>"},
        {
            "type": "text",
            "text": "<existing_posts>\n"
            + (brand.posts or "No post index for this brand yet.")
            + "\n</existing_posts>",
        },
        {
            "type": "text",
            "text": f"<past_interviews>\n{_past_interviews_text(brand)}\n</past_interviews>",
        },
    ]


def interview_system(brand: Brand, template: str) -> list[dict]:
    blocks = [{"type": "text", "text": APP_RULES}]
    blocks += context_blocks(brand)
    blocks.append(
        {
            "type": "text",
            "text": f"<interview_file>\n{template}\n</interview_file>",
            "cache_control": {"type": "ephemeral"},
        }
    )
    return blocks


def kickoff_message(setup: Setup, today: date | None = None) -> str:
    today = today or date.today()
    lines = [
        "Setup details from the person running this interview:",
        f"- Interviewee: {setup.sme_name}",
    ]
    if setup.sme_role:
        lines.append(f"- Role: {setup.sme_role}")
    if setup.sme_expertise:
        lines.append(f"- Expertise: {setup.sme_expertise}")
    if setup.focus_topics:
        lines.append(f"- Focus topics: {setup.focus_topics}")
    lines.append(f"- Time target: {setup.time_target}")
    lines.append(f"- Quick mode: {'on' if setup.quick_mode else 'off'}")
    lines.append(f"- Today's date: {today.isoformat()}")
    lines.append("")
    lines.append("Start the interview.")
    return "\n".join(lines)


IDEA_BANK_RULES = """\
Run the AI Processing Instructions from the interview file below on the
completed interview in the user message. Follow them exactly, plus these app
rules:

1. Site overlap. Check every idea against the existing-post index. Add a
   "Site overlap" line to each card: New, Overlap (name the closest posts and
   say what's still new), or Covered (name the post). Rank Covered ideas Low.
   Start the document with a short overlap table.
2. Keywords. Use only keywords from the target-keywords list. If none fit or
   the list is empty, write "Needs keyword research". Never invent keywords.
3. Client names. {anonymize_rule}
4. Past interviews. If a past interview already produced the same idea, say
   so on the card.
"""

ANONYMIZE_ON = (
    "Replace every name marked [ANON] with a neutral description such as "
    '"a client". This document is meant for the content team to publish from.'
)
ANONYMIZE_OFF = (
    "Keep real names. This copy is internal. Still label [ANON] items "
    '"Needs anonymization before publishing".'
)


def idea_bank_system(brand: Brand, template: str, anonymize: bool) -> list[dict]:
    rules = IDEA_BANK_RULES.format(
        anonymize_rule=ANONYMIZE_ON if anonymize else ANONYMIZE_OFF
    )
    blocks = [{"type": "text", "text": rules}]
    blocks += context_blocks(brand)
    blocks.append(
        {
            "type": "text",
            "text": f"<interview_file>\n{template}\n</interview_file>",
            "cache_control": {"type": "ephemeral"},
        }
    )
    return blocks


# ----------------------------------------------------------- Claude calls


class Turn:
    """One streamed reply. Iterate text_stream(), then read .content and .stop_reason."""

    def __init__(self, client, **request):
        self._client = client
        self._request = request
        self.content: list[dict] = []
        self.stop_reason: str | None = None
        self.text = ""

    def text_stream(self):
        with self._client.beta.messages.stream(**self._request) as stream:
            for chunk in stream.text_stream:
                self.text += chunk
                yield chunk
            message = stream.get_final_message()
        # Keep every block (thinking, fallback, text) so history replays unchanged.
        self.content = [block.to_dict() for block in message.content]
        self.stop_reason = message.stop_reason


def _request(
    model: str, system: list[dict], messages: list[dict], effort: str, max_tokens: int
) -> dict:
    request = dict(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
        output_config={"effort": effort},
        # Also cache the conversation so far, so each new turn reuses it.
        cache_control={"type": "ephemeral"},
    )
    if model not in NO_FALLBACK:
        request.update(betas=[FALLBACK_BETA], fallbacks="default")
    return request


def interview_turn(client, system: list[dict], messages: list[dict], model: str = DEFAULT_MODEL) -> Turn:
    return Turn(client, **_request(model, system, messages, effort="medium", max_tokens=32000))


def idea_bank_turn(client, system: list[dict], interview_md: str, model: str = DEFAULT_MODEL) -> Turn:
    messages = [{"role": "user", "content": f"Completed interview:\n\n{interview_md}"}]
    return Turn(client, **_request(model, system, messages, effort="high", max_tokens=64000))


def text_of(content: list[dict] | str) -> str:
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content if b.get("type") == "text")


def split_interview_file(text: str) -> tuple[str, str | None]:
    """Return (message without the file, file text or None)."""
    match = re.search(re.escape(FILE_START) + r"\s*\n(.*?)\n\s*" + re.escape(FILE_END), text, re.S)
    if not match:
        return text, None
    file_text = match.group(1).strip()
    # Tolerate the model wrapping the file in a code fence anyway.
    file_text = re.sub(r"^```(?:markdown|md)?\n(.*)\n```$", r"\1", file_text, flags=re.S)
    message = (text[: match.start()] + text[match.end():]).strip()
    return message, file_text + "\n"


# --------------------------------------------------------------- storage


@dataclass
class Session:
    brand: str
    template: str
    setup: Setup
    messages: list[dict] = field(default_factory=list)
    status: str = "in progress"  # or "complete"
    id: str = ""
    model: str = DEFAULT_MODEL  # kept for the whole interview, including resume

    @property
    def folder(self) -> Path:
        return OUTPUT_DIR / self.brand / self.id

    def save(self) -> None:
        self.folder.mkdir(parents=True, exist_ok=True)
        data = {
            "brand": self.brand,
            "template": self.template,
            "setup": self.setup.__dict__,
            "messages": self.messages,
            "status": self.status,
            "model": self.model,
            "id": self.id,
            "updated": datetime.now().isoformat(timespec="seconds"),
        }
        (self.folder / "session.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    def save_file(self, name: str, text: str) -> Path:
        self.folder.mkdir(parents=True, exist_ok=True)
        path = self.folder / name
        path.write_text(text, encoding="utf-8")
        return path


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "sme"


def new_session(brand: str, template: str, setup: Setup, model: str = DEFAULT_MODEL) -> Session:
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    session = Session(
        brand, template, setup, id=f"{stamp}-{_slug(setup.sme_name)}-{template}", model=model
    )
    return session


def load_session(path: Path) -> Session:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Session(
        brand=data["brand"],
        template=data["template"],
        setup=Setup(**data["setup"]),
        messages=data["messages"],
        status=data["status"],
        model=data.get("model", DEFAULT_MODEL),
        id=data["id"],
    )


def list_sessions(brand: str, status: str | None = None) -> list[Session]:
    sessions = [load_session(p) for p in sorted((OUTPUT_DIR / brand).glob("*/session.json"))]
    if status:
        sessions = [s for s in sessions if s.status == status]
    return sorted(sessions, key=lambda s: s.id, reverse=True)
