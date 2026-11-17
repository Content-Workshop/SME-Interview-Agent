# SME Interview Prototype

A small app for testing the SME interview agent idea. It runs on your computer and isn't a hosted app.

**What it does**
- Loads a brand: its context, keywords, existing posts and past interviews.
- Interviews an SME in a chat window, one question at a time.
- Asks how an idea differs when it overlaps an existing post.
- Saves the finished interview, then builds an idea bank on request.

**What it skips:** accounts, reminders, full voice interviews, outside clients.

## Set up (once)

You need Python 3.10 or newer and an Anthropic API key.

```bash
cd sme-interview-agent
```

```bash
pip install -r requirements.txt
```

```bash
export ANTHROPIC_API_KEY=your-key-here
```

On Windows, use `set ANTHROPIC_API_KEY=your-key-here` instead of `export`.

## Run it

```bash
streamlit run app.py
```

Your browser opens the app. Fill in the setup form and click **Start interview**.

**To try it without an API key**, run demo mode. It uses canned questions:

```bash
SME_AGENT_DEMO=1 streamlit run app.py
```

## Answering by voice

Click the answer box, then use your computer's built-in dictation:
- **Mac:** press the Fn key twice (or the mic key).
- **Windows:** press Windows + H.

## Where things are saved

Each interview gets a folder under `output/<brand>/`:
- `session.json`: the conversation, saved after every message. Unfinished interviews appear under **Resume** in the sidebar.
- `interview.md`: the completed interview file, with real client names marked `[ANON]`.
- `idea-bank.md`: the idea bank. The sidebar toggle controls whether `[ANON]` names are removed.

`output/` is excluded from git because it can contain real client names.

## Adding a brand

Create a folder under `brands/` with:

| File | What it holds |
|---|---|
| `brand.md` | Brand context. The `## Template fields` list fills the generic interview's placeholders. |
| `keywords.md` | Target keywords. The idea bank uses only these. |
| `posts.md` | Existing-post index. Build it with the command below. |
| `past-interviews/*.md` | Optional earlier interviews to use as context. |

To build the post index from the brand's sitemap:

```bash
python build_post_index.py content-workshop https://contentworkshop.com/post-sitemap.xml
```

## How it decides what to ask

Every interview starts from `templates/generic.md`. The app fills in the brand's fields and the setup form, and the interviewer tailors each question to the SME, the focus topics and the brand context. Brand-specific rules, such as Chatter's `[ROADMAP]` flag, live in each brand's `brand.md`.

The original fixed interviews are kept for reference in `docs/original-interviews/`.

## Project docs

- `docs/sme-agent-requirements.md`: the running requirements list.
- `docs/content-workshop-interview-2026-11-17.md`: the first quick-mode test interview.
- `docs/content-workshop-idea-bank-2026-11-17.md`: the idea bank from that test, with the site overlap check.

## Tests

```bash
python -m unittest discover tests
```

## Model

Pick the model in the sidebar: Sonnet 5.5 (default), Opus 5.5 or Haiku 5.5. A resumed interview keeps its original model. If Sonnet or Opus declines a request, the API retries it on a fallback model automatically (`fallbacks: "default"`); Haiku has no fallback.
