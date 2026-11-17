"""SME interview prototype. Run with:  streamlit run app.py"""

from __future__ import annotations

import os

import streamlit as st

import agent
from agent import GENERIC, Setup

st.set_page_config(page_title="SME Interview", page_icon="🎙️", layout="centered")

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


# ---------------------------------------------------------------- sidebar

with st.sidebar:
    st.header("Setup")
    brands = agent.list_brands()
    brand_slug = st.selectbox(
        "Brand",
        brands,
        index=brands.index("content-workshop") if "content-workshop" in brands else 0,
        format_func=lambda s: agent.load_brand(s).name,
        key="brand",
    )
    brand = agent.load_brand(brand_slug)
    st.caption(
        f"{len(brand.posts.split(chr(10) + '## ')) - 1 if brand.posts else 0} existing posts · "
        f"{len(brand.past_interviews)} past interviews loaded"
    )

    in_progress = agent.list_sessions(brand_slug, status="in progress")
    if in_progress:
        st.subheader("Resume an interview")
        by_id = {s.id: s for s in in_progress}
        choice = st.selectbox(
            "In-progress interviews",
            [""] + list(by_id),
            format_func=lambda i: "Choose one" if not i else f"{by_id[i].setup.sme_name} · {i[:15]}",
        )
        if choice and st.button("Resume"):
            st.session_state.session = by_id[choice]
            st.rerun()

    st.subheader("Model")
    model = st.selectbox(
        "Model for new interviews",
        list(agent.MODELS),
        index=list(agent.MODELS).index(agent.DEFAULT_MODEL),
        format_func=agent.MODELS.get,
        help="Costs are rough estimates. A resumed interview keeps the model it started with.",
    )

    st.subheader("Outputs")
    anonymize = st.toggle(
        "Anonymize client names in the idea bank",
        value=True,
        help="The interview record always keeps real names for you. "
        "This controls the idea bank, which is meant for publishing.",
    )

    if "session" in st.session_state and st.button("Start a new interview"):
        del st.session_state["session"]
        st.rerun()

    if DEMO:
        st.info("Demo mode: replies are canned, no API key used.")

st.title("SME Interview")

if not has_credentials():
    st.error(
        "No Anthropic API key found. Set ANTHROPIC_API_KEY and restart the app, "
        "or run in demo mode with SME_AGENT_DEMO=1. See README.md."
    )
    st.stop()

client = get_client()

# ------------------------------------------------------------ setup form

if "session" not in st.session_state:
    st.write(f"Set up an interview for **{brand.name}**.")
    with st.form("setup"):
        sme_name = st.text_input("SME name *")
        sme_role = st.text_input("Role", placeholder="e.g. VP of Threat Intelligence")
        sme_expertise = st.text_input(
            "What they know best", placeholder="2 to 4 areas, separated by commas"
        )
        core_task = st.text_input(
            "A core task others could learn from",
            help="Used for the step-by-step process question.",
        )
        focus_topics = st.text_area(
            "Focus topics",
            placeholder="What should this interview cover? e.g. AI search, SME interviews",
            help="The interviewer leans its questions toward these.",
        )
        time_target = st.radio("Length", TIME_TARGETS, index=1, horizontal=True)
        quick_mode = st.checkbox("Quick mode (priority questions only, about 10 minutes)")
        started = st.form_submit_button("Start interview", type="primary")

    if started:
        if not sme_name.strip():
            st.warning("Add the SME's name to start.")
            st.stop()
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
        st.session_state.session = session
        st.rerun()
    st.stop()

# --------------------------------------------------------------- interview

session: agent.Session = st.session_state.session
brand = agent.load_brand(session.brand)
template = agent.template_for(brand, session.setup)
system = agent.interview_system(brand, template)

st.caption(
    f"{brand.name} · {session.setup.sme_name} · "
    f"{agent.MODELS.get(session.model, session.model).split(' (')[0]}"
)


def show_assistant(text: str) -> None:
    message, file_text = agent.split_interview_file(text)
    st.markdown(message)
    if file_text:
        st.success("Interview complete. The file is saved.")


for msg in session.messages[1:]:  # skip the hidden setup message
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            show_assistant(agent.text_of(msg["content"]))
        else:
            st.markdown(msg["content"])


def run_turn() -> None:
    turn = agent.interview_turn(client, system, session.messages, session.model)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        shown = ""
        for chunk in turn.text_stream():
            shown += chunk
            # Hide the raw file while it streams in.
            placeholder.markdown(shown.split(agent.FILE_START)[0] + " ▌")
        placeholder.empty()
        show_assistant(turn.text)
    session.messages.append({"role": "assistant", "content": turn.content})
    if turn.stop_reason == "refusal":
        st.warning("The model declined that message. Try rephrasing your answer.")
    _, file_text = agent.split_interview_file(turn.text)
    if file_text:
        session.save_file("interview.md", file_text)
        session.status = "complete"
    session.save()


# Claude replies whenever the last message is the interviewee's
# (the hidden setup message, a new answer, or a resumed interview).
if session.status != "complete" and session.messages[-1]["role"] == "user":
    try:
        run_turn()
    except Exception as error:  # show API problems instead of a blank page
        st.error(f"Couldn't reach Claude: {error}")

interview_path = session.folder / "interview.md"
idea_bank_path = session.folder / "idea-bank.md"

if session.status == "complete" and interview_path.is_file():
    st.divider()
    st.subheader("Results")
    st.caption(f"Saved in {session.folder}")
    st.download_button(
        "Download interview", interview_path.read_text(encoding="utf-8"),
        file_name=f"{session.id}-interview.md",
    )
    if idea_bank_path.is_file():
        st.download_button(
            "Download idea bank", idea_bank_path.read_text(encoding="utf-8"),
            file_name=f"{session.id}-idea-bank.md",
        )
        with st.expander("Idea bank", expanded=True):
            st.markdown(idea_bank_path.read_text(encoding="utf-8"))
    elif st.button("Build idea bank", type="primary"):
        turn = agent.idea_bank_turn(
            client,
            agent.idea_bank_system(brand, template, anonymize),
            interview_path.read_text(encoding="utf-8"),
            session.model,
        )
        with st.spinner("Building the idea bank. This can take a few minutes..."):
            for _ in turn.text_stream():
                pass
        if turn.stop_reason == "refusal":
            st.warning("The model declined to build the idea bank.")
        else:
            session.save_file("idea-bank.md", turn.text)
            st.rerun()
else:
    st.caption(DICTATION_TIP)
    answer = st.chat_input("Type or dictate your answer")
    if answer:
        session.messages.append({"role": "user", "content": answer})
        session.save()
        st.rerun()
