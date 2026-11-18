# SME Interview Agent: Dev Team Rundown

**As of:** 2026-11-18
**Repo:** `content-workshop/sme-interview-agent`, branch `staging`
**Status:** working prototype, tested on one machine, not yet hosted

---

## The ask

I'd like your direction on four things before going further:

1. **Hosting:** is Streamlit Community Cloud fine for a small test, or should this live somewhere we already run?
2. **Storage:** where should interviews and results be saved so they don't get wiped?
3. **Security:** is the current access model (password for setup, secret link per SME) good enough for a test with real people?
4. **Direction:** should this stay a standalone tool, or become part of Chatter?

A 30-minute review of the repo and this doc would be enough to start.

---

## What it is

An AI interviewer that gets expert knowledge out of a subject-matter expert (SME) without a live interview.

1. Someone sets up an interview: the brand, the SME, and the focus topics.
2. The SME gets a link and answers questions in a chat window, typing or dictating.
3. The AI asks one question at a time, with one follow-up at most, and checks answers against the brand's existing posts.
4. The finished interview is saved, and an "idea bank" of ranked content ideas can be generated from it.

**Why:** SMEs have the knowledge but no time for meetings. The longer-term idea is a tool clients could use, possibly inside Chatter.

**Where it came from:** a Markdown interview template that you attach to any AI chat. That works, but it can't read brand context, check existing content, store results, or be sent to someone else. This prototype tests those missing pieces.

---

## What's built

| Feature | Status |
|---|---|
| Load a brand: context, keywords, existing posts, past interviews | Built |
| Post index built from the brand's sitemap (Content Workshop: 148 posts) | Built |
| Interview tailored to the SME and focus topics | Built |
| Asks how an idea differs when it overlaps an existing post | Built |
| Setup page creates a private link per SME; SME sees only the chat | Built |
| Progress saved after every answer; SME can close and reopen the link | Built |
| Idea bank generated from a finished interview, with site-overlap check | Built |
| Client names: kept internally, optionally anonymized in the idea bank | Built |
| Model picker: Sonnet 5.5 (default), Opus 5.5, Haiku 5.5 | Built |
| Voice answers via the computer's built-in dictation | Works, no build needed |
| Demo mode with canned replies (no API key) | Built |
| Hosting | **Not done** |
| Durable storage | **Not done** |
| Reminder emails | Later version |
| Full voice interviews (AI speaks too) | Later version |

---

## How it works

**Stack:** Python 3.10+, Streamlit (UI), Anthropic Python SDK (Claude API). No database.

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI. Two views: setup (no URL parameter) and interview (`?interview=<token>`). |
| `agent.py` | Everything else: brand loading, prompt building, Claude calls, saving sessions. No Streamlit imports. |
| `build_post_index.py` | Reads a sitemap, fetches each post, writes title, summary, headings and opening lines to `brands/<brand>/posts.md`. |
| `demo_client.py` | Fake Claude client for demo mode and tests. |
| `templates/generic.md` | The interview template every interview starts from. |
| `brands/<brand>/` | `brand.md` (context and rules), `keywords.md`, `posts.md`, `past-interviews/`. |
| `tests/test_agent.py` | 13 unit tests, standard library only. |

**Claude API usage**
- Each turn is one streamed Messages API call.
- The system prompt holds app rules, brand context, keywords, the post index, past interviews and the filled template. It's about 187K characters, which is mostly the post index.
- Prompt caching is on for the system prompt and the conversation, so each turn after the first mostly reads from cache.
- Server-side refusal fallback is on for Sonnet and Opus. Haiku has no fallback.
- The interview ends when the model outputs the completed file between marker lines. The app detects the markers and saves the file.

**Storage**
- `output/<brand>/<session-id>/` holds `session.json` (full message history and setup), `interview.md` and `idea-bank.md`.
- `output/` is gitignored because it can contain real client names.

**Access**
- Setup page: optional `APP_PASSWORD`.
- SME links: a 16-byte random token per interview, compared with a constant-time check.
- No user accounts.

**Estimated cost per interview** (my estimates, not measured): Sonnet $0.50 to $1, Opus $1 to $2, Haiku a few cents.

---

## What's tested

| Area | Result |
|---|---|
| Unit tests (13) | Pass |
| Full flow in demo mode: setup, link, SME chat, finish, idea bank (headless browser) | Pass |
| API request shape against the real SDK, with a mocked HTTP layer | Pass |
| Live run with a real API key | Started on my Mac; full interview not finished yet |
| Interview quality with a real SME other than me | Not tested |
| Hosted deployment | Not tested |

---

## Open questions for the dev team

1. **Hosting.** Streamlit Community Cloud is free and deploys from GitHub. But it can wipe files on restart, needs access to the Content-Workshop GitHub org, and is public apart from the password. Is that OK for a test, or is there a better option?
2. **Storage.** Interviews are local JSON and Markdown files. What should replace them: a database, cloud storage, or Google Drive?
3. **API key.** It's an environment variable or Streamlit secret. Is there a company key or account we should use, and who owns billing?
4. **Security and privacy.** Interviews can include client names and confidential details. What's the minimum bar for a test with external SMEs: authentication, data retention, access logs?
5. **Stack.** Is Streamlit fine for a prototype, or should a real version be built in whatever Chatter uses?
6. **Chatter fit.** If this becomes part of Chatter, what would need to change: auth, storage, brand data, post indexing?
7. **Post index.** It's built from page HTML by a script and refreshed by hand. Should it run on a schedule, or come from an existing Chatter data source?

---

## Requirements list

Full list: `docs/sme-agent-requirements.md`.

| # | Requirement | Status |
|---|---|---|
| 1 | Check ideas against existing posts | In prototype |
| 2 | Read existing context first | In prototype |
| 3 | Contextual follow-ups (one max) | Validated in first test |
| 4 | Store interviews and idea banks | Local files only |
| 5 | Quick mode actually skips follow-ups | In prototype, untested live |
| 6 | Voice-to-text answers | Works via built-in dictation |
| 7 | Anonymization toggle | In prototype |
| 8 | Keywords in brand context | In prototype; keyword list still empty |
| 9 | Loadable brands | In prototype (Content Workshop, Chatter) |
| 10 | Reminder emails | Later version; needs hosting and accounts |
| 11 | Choose interview topics | In prototype |
| 12 | Separate setup from the interview (link) | In prototype; needs hosting |
| 13 | No generic questions | In prototype, untested live |

---

## How to run it locally

Clone the `staging` branch, then:

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
export ANTHROPIC_API_KEY=your-key
```

```bash
streamlit run app.py
```

To try it without a key: `SME_AGENT_DEMO=1 streamlit run app.py`. Run the tests with `python -m unittest discover tests`. The README has the details.

**Other docs in `docs/`:** the requirements list, the first test interview and its idea bank, and the original fixed interview templates.
