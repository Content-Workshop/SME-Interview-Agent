"""SME interview prototype. Run with:  streamlit run app.py

Two views:
- Setup (no link parameter): you set up interviews, copy each SME's link,
  and collect results. Protected by APP_PASSWORD when it is set.
- Interview (?interview=<token>): what the SME sees. Only the chat.
"""

from __future__ import annotations

import os

import streamlit as st

import agent
from agent import GENERIC, Setup

st.set_page_config(page_title="SME Interview", page_icon="🎙️", layout="centered")

# On Streamlit Community Cloud, settings come from the app's Secrets.
for _key in ("ANTHROPIC_API_KEY", "APP_PASSWORD", "APP_URL"):
    try:
        if _key in st.secrets and not os.environ.get(_key):
            os.environ[_key] = str(st.secrets[_key])
    except Exception:  # no secrets file when running locally
        break

DEMO = os.environ.get("SME_AGENT_DEMO") == "1"
if DEMO:  # keep canned demo runs out of the real interview history
    agent.OUTPUT_DIR = agent.ROOT / "output-demo"
TIME_TARGETS = ["About 15 minutes", "20 to 30 minutes", "45 to 60 minutes"]
DICTATION_TIP = (
    "🎤 To answer by voice, click the answer box, then use your computer's dictation: "
    "**Mac:** press the Fn key twice · **Windows:** press Windows + H."
)


@st.cache_resource
def get_client():
    if DEMO:
        from demo_client import DemoClient

        return DemoClient()
    import anthropic

    return anthropic.Anthropic()


def has_credentials() -> bool:
    return DEMO or bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))


def require_credentials() -> None:
    if not has_credentials():
        st.error(
            "No Anthropic API key found. Set ANTHROPIC_API_KEY and restart the app, "
            "or run in demo mode with SME_AGENT_DEMO=1. See README.md."
        )
        st.stop()


def interview_link(session: agent.Session) -> str:
    base = os.environ.get("APP_URL") or (st.context.url or "").split("?")[0]
    return f"{base.rstrip('/')}/?interview={session.token}"


def model_name(model: str) -> str:
    return agent.MODELS.get(model, model).split(" (")[0]


# ================================================================ SME view


def interview_view(token: str) -> None:
    session = agent.find_session(token)
    if session is None:
        st.title("Interview not found")
        st.write("This link doesn't match an interview. Check with the person who sent it.")
        st.stop()
    require_credentials()
    client = get_client()
    brand = agent.load_brand(session.brand)
    template = agent.template_for(brand, session.setup)
    system = agent.interview_system(brand, template)

    st.title(f"{brand.name} interview")
    st.caption(f"For {session.setup.sme_name}. Your progress saves after every answer.")

    def show_assistant(text: str) -> None:
        message, file_text = agent.split_interview_file(text)
        st.markdown(message)
        if file_text:
            st.success("You're all done. Thank you! You can close this window.")

    for msg in session.messages[1:]:  # skip the hidden setup message
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                show_assistant(agent.text_of(msg["content"]))
            else:
                st.markdown(msg["content"])

    # Claude replies whenever the last message is the SME's: the hidden setup
    # message (first visit), a new answer, or an answer left unanswered.
    if session.status != "complete" and session.messages[-1]["role"] == "user":
        try:
            turn = agent.interview_turn(client, system, session.messages, session.model)
            with st.chat_message("assistant"):
                placeholder = st.empty()
                shown = ""
                for chunk in turn.text_stream():
                    shown += chunk
                    # Hide the raw interview file while it streams in.
                    placeholder.markdown(shown.split(agent.FILE_START)[0] + " ▌")
                placeholder.empty()
                show_assistant(turn.text)
            session.messages.append({"role": "assistant", "content": turn.content})
            if turn.stop_reason == "refusal":
                st.warning("The interviewer couldn't respond to that. Try rephrasing your answer.")
            _, file_text = agent.split_interview_file(turn.text)
            if file_text:
                session.save_file("interview.md", file_text)
                session.status = "complete"
            session.save()
        except Exception as error:  # show API problems instead of a blank page
            st.error(f"Something went wrong reaching the interviewer. Refresh to try again. ({error})")

    if session.status != "complete":
        st.caption(DICTATION_TIP)
        answer = st.chat_input("Type or dictate your answer")
        if answer:
            session.messages.append({"role": "user", "content": answer})
            session.save()
            st.rerun()


# ============================================================== setup view


def password_gate() -> None:
    password = os.environ.get("APP_PASSWORD")
    if not password or st.session_state.get("signed_in"):
        return
    st.title("SME Interview")
    entered = st.text_input("Password", type="password")
    if entered:
        if entered == password:
            st.session_state.signed_in = True
            st.rerun()
        st.error("That password isn't right.")
    st.stop()


def setup_view() -> None:
    password_gate()

    with st.sidebar:
        st.header("Settings")
        brands = agent.list_brands()
        brand_slug = st.selectbox(
            "Brand",
            brands,
            index=brands.index("content-workshop") if "content-workshop" in brands else 0,
            format_func=lambda s: agent.load_brand(s).name,
        )
        brand = agent.load_brand(brand_slug)
        post_count = brand.posts.count("\n## ") if brand.posts else 0
        st.caption(f"{post_count} existing posts · {len(brand.past_interviews)} past interviews loaded")
        model = st.selectbox(
            "Model for new interviews",
            list(agent.MODELS),
            index=list(agent.MODELS).index(agent.DEFAULT_MODEL),
            format_func=agent.MODELS.get,
            help="Costs are rough estimates. Each interview keeps the model it was set up with.",
        )
        anonymize = st.toggle(
            "Anonymize client names in the idea bank",
            value=True,
            help="The interview record always keeps real names for you. "
            "This controls the idea bank, which is meant for publishing.",
        )
        if DEMO:
            st.info("Demo mode: replies are canned, no API key used.")

    st.title("SME Interview")
    require_credentials()

    # ---- new interview
    st.subheader(f"Set up an interview for {brand.name}")
    with st.form("setup", clear_on_submit=True):
        sme_name = st.text_input("SME name *")
        sme_role = st.text_input("Role", placeholder="e.g. VP of Threat Intelligence")
        sme_expertise = st.text_input("What they know best", placeholder="2 to 4 areas, separated by commas")
        core_task = st.text_input(
            "A process they could walk someone through",
            placeholder="e.g. turning an SME brain dump into a content brief",
            help='Sets up the question "Walk me through how you do this, step by step." '
            "Leave blank to ask about their core work in general.",
        )
        focus_topics = st.text_area(
            "Focus topics",
            placeholder="What should this interview cover? e.g. AI search, SME interviews",
            help="The interviewer leans its questions toward these.",
        )
        time_target = st.radio("Length", TIME_TARGETS, index=1, horizontal=True)
        quick_mode = st.checkbox("Quick mode (priority questions only, about 10 minutes)")
        created = st.form_submit_button("Create interview link", type="primary")

    if created:
        if not sme_name.strip():
            st.warning("Add the SME's name first.")
        else:
            setup = Setup(
                sme_name=sme_name.strip(),
                sme_role=sme_role.strip(),
                sme_expertise=sme_expertise.strip(),
                core_task=core_task.strip(),
                focus_topics=focus_topics.strip(),
                time_target=time_target,
                quick_mode=quick_mode,
            )
            session = agent.new_session(brand_slug, GENERIC, setup, model)
            session.messages.append({"role": "user", "content": agent.kickoff_message(setup)})
            session.save()
            st.success(f"Interview for {setup.sme_name} is ready. Send them this link:")
            st.code(interview_link(session), language=None)
            st.caption("Copy it with the button on the right. The interview starts when they open it.")

    # ---- existing interviews
    st.divider()
    st.subheader("Interviews")
    sessions = agent.list_sessions(brand_slug)
    if not sessions:
        st.caption("None yet.")
    client = get_client()
    template_cache: dict[str, str] = {}
    for session in sessions:
        if session.status == "complete":
            status = "✅ Complete"
        elif session.started:
            status = "💬 In progress"
        else:
            status = "✉️ Not started"
        with st.expander(f"{session.setup.sme_name} · {status} · {session.id[:10]}"):
            st.caption(f"Model: {model_name(session.model)}")
            st.write("Interview link:")
            st.code(interview_link(session), language=None)
            interview_path = session.folder / "interview.md"
            idea_bank_path = session.folder / "idea-bank.md"
            if not interview_path.is_file():
                continue
            st.download_button(
                "Download interview",
                interview_path.read_text(encoding="utf-8"),
                file_name=f"{session.id}-interview.md",
                key=f"dl-int-{session.id}",
            )
            if idea_bank_path.is_file():
                st.download_button(
                    "Download idea bank",
                    idea_bank_path.read_text(encoding="utf-8"),
                    file_name=f"{session.id}-idea-bank.md",
                    key=f"dl-idea-{session.id}",
                )
                st.markdown(idea_bank_path.read_text(encoding="utf-8"))
            elif st.button("Build idea bank", type="primary", key=f"build-{session.id}"):
                if session.id not in template_cache:
                    template_cache[session.id] = agent.template_for(brand, session.setup)
                turn = agent.idea_bank_turn(
                    client,
                    agent.idea_bank_system(brand, template_cache[session.id], anonymize),
                    interview_path.read_text(encoding="utf-8"),
                    session.model,
                )
                with st.spinner("Building the idea bank. This can take a few minutes..."):
                    try:
                        for _ in turn.text_stream():
                            pass
                    except Exception as error:
                        st.error(f"Couldn't reach Claude: {error}")
                        st.stop()
                if turn.stop_reason == "refusal":
                    st.warning("The model declined to build the idea bank.")
                else:
                    session.save_file("idea-bank.md", turn.text)
                    st.rerun()


# ==================================================================== main

token = st.query_params.get("interview")
if token:
    interview_view(token)
else:
    setup_view()
