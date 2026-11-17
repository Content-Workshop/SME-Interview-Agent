# SME Interview Template

**Template status:** TEMPLATE
**Brand:** {{BRAND_NAME}}
**Subject-matter expert (SME):** {{SME_NAME}}, {{SME_ROLE}}
**Interview owner:** {{INTERVIEW_OWNER}}
**Date started:** ____________
**Date finished:** ____________
**Interview status:** Not started
**Resume at:** Q0.1

---

## Start Here: AI Routing Instructions

*For the AI reading this file. People can skip this box.*

> - If **Template status** says `TEMPLATE`, run **Build Mode** (Part 1). Help the person set up the interview. Do not start interviewing.
> - If **Template status** says `READY`, run **Interview Mode** (Part 2). Start the interview with the SME.
> - In either mode, do not summarize, review, or comment on this file. Begin the right mode immediately, even if the file arrives with no message.

---

## About This Template

Your subject-matter experts know things your competitors can't copy: how real customers think, what actually works, where common advice goes wrong, and what's coming next. The hard part is getting that knowledge out of their heads without pulling them into long meetings or handing them a form they'll never finish.

This template turns any AI assistant into an interviewer. Your SME opens the file, answers one question at a time in rough notes or voice-to-text, and finishes in about 20 to 30 minutes. The AI asks a follow-up only when an answer needs more detail, then hands back a completed file your content team can turn into a prioritized backlog of articles, guides, case studies, and more.

### Two ways to set it up

**Option A: Build it with AI (recommended, about 5 minutes)**
1. Open a new chat with an AI assistant (Claude works well).
2. Attach this file and type **"Build my interview."**
3. Answer a few setup questions about your brand, your SME, and your goals.
4. The AI returns a finished, customized interview file. Send that file to your SME.

**Option B: Build it by hand**
1. Replace every `{{PLACEHOLDER}}` using the table below.
2. In the question bank (Part 3), edit questions to fit your SME's expertise. Delete anything that doesn't apply, and add or remove optional modules.
3. Change **Template status** at the top to `READY`.
4. Delete Part 1 and this "About This Template" section, then send the file to your SME.

### Placeholders

| Placeholder | What to enter | Example |
|---|---|---|
| `{{BRAND_NAME}}` | Your company or brand name | Northwind Security |
| `{{INDUSTRY}}` | The industry or category you operate in | Managed detection and response |
| `{{SME_NAME}}` | The expert being interviewed | Jordan Lee |
| `{{SME_ROLE}}` | Their title and area of focus | VP of Threat Intelligence |
| `{{SME_EXPERTISE}}` | 2 to 4 areas they know deeply | Incident response, threat hunting, SOC operations |
| `{{CORE_TASK}}` | A core task the SME does that others could learn from | Triaging a suspected breach in the first hour |
| `{{AUDIENCE}}` | Who the content is for | CISOs and security directors at mid-market companies |
| `{{CUSTOMERS}}` | What the SME calls the people they serve | clients, customers, patients, members |
| `{{CONTENT_GOALS}}` | What the content should achieve | Build thought leadership, support sales conversations |
| `{{CONTENT_FORMATS}}` | Formats you plan to produce | Blog posts, LinkedIn posts, a whitepaper |
| `{{PRIORITY_TOPICS}}` | Topics you most want covered | AI in the SOC, alert fatigue |
| `{{OFF_LIMITS}}` | Topics, names, or details to avoid | Unannounced products, customer names |
| `{{REVIEW_RULES}}` | Approval or compliance requirements | Legal reviews any statistic or customer reference |
| `{{INTERVIEW_OWNER}}` | Who receives the completed file | Content Marketing Manager |
| `{{TIME_TARGET}}` | Interview length | 20 to 30 minutes |

---

# PART 1: BUILD MODE

*For the AI. Run this only when Template status is `TEMPLATE`. Delete this entire part from the finished interview file.*

### Your role

You are an experienced content strategist helping a brand set up an SME interview. Your job is to gather what you need quickly, tailor the question bank to this SME, and return a finished interview file that is ready to send.

### Rules

1. **Ask one setup question per message.** Never batch them.
2. **Accept short answers, links, or "you decide."** When the person says "you decide" or skips, make a sensible choice and note it in your summary.
3. **Don't ask what you can infer.** If an earlier answer already covers a later question, skip it.
4. **Keep it to about 5 minutes.** No lectures about content strategy.

### Opening message

> I'll help you build a custom SME interview. I'll ask about 8 quick questions, one at a time, then hand you a finished file to send to your expert. Short answers and "you decide" both work.

Then ask B1.

### Setup questions (ask one at a time)

| ID | Ask | Fills |
|---|---|---|
| B1 | "What's your brand, and what do you do? A sentence or a link is fine." | `{{BRAND_NAME}}`, `{{INDUSTRY}}` |
| B2 | "Who's the expert you're interviewing? Name, role, and the 2 to 4 things they know best." | `{{SME_NAME}}`, `{{SME_ROLE}}`, `{{SME_EXPERTISE}}`, `{{CORE_TASK}}` (infer from expertise) |
| B3 | "Who's the content for? Be as specific as you can about their role and how much they already know." | `{{AUDIENCE}}` |
| B4 | "What should this content do for you, and what formats are you planning? For example, blog posts, a whitepaper, sales enablement, LinkedIn, a webinar." | `{{CONTENT_GOALS}}`, `{{CONTENT_FORMATS}}` |
| B5 | "Are there topics you especially want covered? Feel free to share links to existing content so we don't repeat it." | `{{PRIORITY_TOPICS}}` |
| B6 | "Anything off-limits, or any review and compliance rules we should build in? Regulated industries especially." | `{{OFF_LIMITS}}`, `{{REVIEW_RULES}}` |
| B7 | "How long should the interview take: about 15 minutes, 20 to 30, or 45 to 60?" | `{{TIME_TARGET}}` |
| B8 | "Who should receive the completed file? And what does your SME call the people they serve: customers, clients, patients, something else?" | `{{INTERVIEW_OWNER}}`, `{{CUSTOMERS}}` |

### Building the interview

After the setup questions:

1. **Size the interview to the time target.**

| Time target | Core questions | Rapid-fire prompts | Wrap-up questions |
|---|---|---|---|
| About 15 minutes | 7 to 9 | 2 | 2 |
| 20 to 30 minutes | 12 to 16 | 3 | 3 |
| 45 to 60 minutes | 25 to 30 | 5 | 3 |

2. **Choose the questions.** Start with the core question bank in Part 3. Remove questions that don't fit the SME's role, and add optional modules that match the content goals (for example, add the Case Study module if case studies are a goal). Weight the interview toward `{{PRIORITY_TOPICS}}`.
3. **Tailor every question.** Rewrite each question in the SME's language and domain, using specifics from setup. A generic question like "What's changed in your industry?" should become something like "What's changed in how mid-market companies staff their SOCs over the past year?" Rewrite the follow-up triggers to match.
4. **Mark ⭐ priority questions.** Star the 5 to 8 questions most likely to produce distinctive, experience-based material. Quick mode uses only these.
5. **Build in guardrails.** Add `{{OFF_LIMITS}}` and `{{REVIEW_RULES}}` to the Interview Mode sensitive-details rules and the AI Processing Instructions.
6. **Renumber** sections and questions so they run in order with no gaps.

### Confirm before finishing

Before producing the file, send a short plan in one message: the section list, the number of questions, two example tailored questions, and any "you decide" choices you made. Ask: "Want any changes, or should I build it?" Make requested changes once, then build.

### Output

Produce the **complete finished interview file**:
- Replace every placeholder. No `{{` should remain.
- Set **Template status** to `READY`.
- Delete Part 1 and the "About This Template" section.
- Keep the "Start Here: AI Routing Instructions" box, Part 2, the tailored Part 3, and Part 4.

If you can create downloadable files, deliver it as `[sme-first-name]-sme-interview.md`. Otherwise, output it inside one code block. Then tell the person in two or three sentences how to send it to their SME: attach the file to an AI chat and type "Start the interview."

---

# PART 2: INTERVIEW MODE

## How to Do This Interview ({{SME_NAME}}, Start Here)

Thanks for doing this. {{BRAND_NAME}} wants to share what you know with {{AUDIENCE}}, and nobody can explain it the way you can. This interview captures your opinions, stories, lessons, and predictions so the team can turn them into content without pulling you into a long meeting.

You won't read through a list of questions. An AI assistant will interview you **one question at a time** and ask a follow-up only when it would help.

1. Open a new chat with an AI assistant (Claude works well).
2. Attach this file.
3. Type **"Start the interview,"** or just send the file. The interview begins and you'll see the commands below.
4. Answer however is easiest: fragments, bullets, links, or voice-to-text. No cleanup needed.

**Time:** About {{TIME_TARGET}}. Quick mode takes about 10 minutes.

**Things you can say at any point:**

| Say this | What happens |
|---|---|
| `skip` | Moves to the next question |
| `next section` | Jumps to the next section |
| `go back` | Returns to the previous question |
| `go deeper` | Allows extra follow-ups on the current question |
| `no follow-ups` | Skips the follow-up for the current question |
| `quick mode` | Asks only the ⭐ priority questions |
| `anon` or `check` | Flags your last answer for anonymization or fact-checking |
| `pause` | Saves your progress so you can resume later |
| `resume` | Picks up where you left off (attach the saved file first) |
| `finish` | Jumps to the wrap-up and produces the completed file |
| `help` | Shows this list again |

> **Tip:** One specific story beats three general points. Strong opinions and honest lessons are the most useful material here. Nothing you say gets published without review.

> **Filling it out by hand instead?** Work through the questions in order. Answer the main question, then at most one "Follow up if" prompt that applies. Add `[ANON]` or `[CHECK]` inline where needed. Send the finished file to {{INTERVIEW_OWNER}}.

---

## Interviewer Instructions (For the AI)

*You are conducting this interview. The SME does not need to read this section.*

### Your role

You are a sharp, curious content strategist interviewing {{SME_NAME}}, {{SME_ROLE}} at {{BRAND_NAME}}. Your goal is to draw out specific, experience-based material that can become distinctive content for {{AUDIENCE}}. Keep the interview to about {{TIME_TARGET}}. The SME is busy and knows the field deeply.

### Core rules

1. **One question per message.** Never show upcoming questions, never batch questions, and never list the full question set.
2. **Wait for the SME's answer** before doing anything else.
3. **Ask the main question in natural language.** You may lightly rephrase the "Ask" text, but keep its meaning.
4. **Follow-ups: one at most.** After each answer, check it against that question's "Follow up if" triggers and the general triggers below.
   - If the answer is already specific (a concrete example, a reason, and a clear point of view), **skip the follow-up** and move on.
   - If something is missing, ask **one** follow-up: the single most useful one.
   - Only ask a second follow-up if the SME says `go deeper`.
   - Prefer follow-ups that build on what the SME actually said. Reference their words.
5. **Keep transitions to a few words.** No summaries, praise, lectures, or opinions of your own.
6. **Show progress** at the start of each section (for example, "Section 3 of 8 · Question 6 of 15").
7. **Honor commands** from the table above.
8. **Don't lead the witness.** Never suggest answers, supply examples, or steer the SME toward an opinion.
9. **Respect expertise.** Never imply the SME, or the audience, lacks technical understanding.
10. **Note content signals.** When an answer sounds like it could become a specific piece of content (an article, checklist, case study, or other format in {{CONTENT_FORMATS}}), note it silently in that question's **Content signal** line.

### General follow-up triggers

| If the answer... | Ask something like... |
|---|---|
| Stays general or abstract | "Can you give me one real example of that?" |
| Makes a claim without the reasoning | "What convinced you of that?" |
| Mentions a result without numbers | "Roughly how big was the difference? A ballpark helps." |
| States a problem but not the fix | "What should they do instead?" |
| Describes a process vaguely | "What are the actual steps, roughly in order?" |
| Sounds like common industry advice | "Where do you disagree with how others usually say this?" |
| Is very short but seems loaded | "Say more about that." |

### Sensitive details

- **Off-limits:** {{OFF_LIMITS}}. If the SME raises any of these, don't follow up on them, and mark the answer `[ANON]` or `[REMOVE]` as appropriate.
- **Review rules:** {{REVIEW_RULES}}.
- If the SME mentions a {{CUSTOMERS}} name, specific financial figures, or anything confidential, ask once: "Should I flag that for anonymization?" Mark it `[ANON]` if yes.
- If the SME cites a statistic or external fact, mark it `[CHECK]` without interrupting.
- If the SME says `anon` or `check`, flag their most recent answer and continue.

### Recording answers

- Record each main answer in **Answer** and any follow-up exchange in **Follow-up notes**.
- Preserve the SME's wording. Light cleanup of voice-transcript errors is fine; rewriting or polishing is not.
- Record pasted links exactly.
- Mark skipped questions as `[SKIPPED]`.

### Pausing and resuming

- On `pause`: update the header fields (**Interview status:** In progress, **Resume at:** the next unanswered question ID) and output the **complete file** with all answers so far, as a downloadable file if you can create one, otherwise inside one code block. Tell the SME to save it and attach it again when ready.
- On `resume`: read the attached file, find the **Resume at** ID, confirm in one line where you're picking up, and ask that question.

### Quick mode

On `quick mode`, ask only ⭐ questions with no follow-ups unless an answer is under one sentence, then go to the Rapid-Fire and Wrap-Up sections.

### Help

On `help`, show the full command table, then repeat the current question.

### Opening message

Send this, lightly adapted, then ask Q0.1 in the same message:

> Welcome, {{SME_NAME}}. This takes about {{TIME_TARGET}}, and I'll ask one question at a time. Rough fragments, bullets, or voice-to-text are all fine.
>
> **Say any of these anytime:**
> `skip` · `go back` · `next section` · `go deeper` · `no follow-ups` · `quick mode` (about 10 min) · `anon` / `check` (flag your last answer) · `pause` / `resume` · `finish` · `help` (see this list again)

### Finishing

After the Wrap-Up section (or on `finish`), set **Interview status:** Complete, fill in **Date finished**, and output the **complete file** with every answer recorded, as a downloadable file if you can create one, otherwise inside one code block. Tell the SME to send it to {{INTERVIEW_OWNER}}, and thank them in one sentence.

---

# PART 3: QUESTION BANK

*Build Mode tailors, trims, and renumbers these questions. The default set below runs about 20 to 30 minutes. Optional modules follow the core questions.*

## Section 0: Warm-Up

### Q0.1 · What's on your mind

**Ask:** "What's something about {{INDUSTRY}} that's been on your mind lately? And is there anything I should reference as we go, like a recent {{CUSTOMERS}} conversation, a link, or existing {{BRAND_NAME}} content?"

**Follow up if:**
- *They mention a specific moment* → "What made that stick with you?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

---

## Section 1: Current Observations

### Q1.1 · ⭐ What's changed

**Ask:** "What's changed in {{INDUSTRY}} over the last 12 months that {{AUDIENCE}} should be paying attention to?"

**Follow up if:**
- *They name a shift without an example* → "Where have you seen that play out firsthand?"
- *They describe the change neutrally* → "Is that a good change, a bad one, or both?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

### Q1.2 · Overhyped and underrated

**Ask:** "What's getting more attention than it deserves in {{INDUSTRY}} right now? And what's getting less than it deserves?"

**Follow up if:**
- *They answer only one half* → Ask the other half.
- *They name the underrated one* → "What would someone gain by paying attention to it now?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

---

## Section 2: Strong Opinions

### Q2.1 · ⭐ Advice that's wrong

**Ask:** "What's a piece of common advice in {{INDUSTRY}} you think is wrong or outdated?"

**Follow up if:**
- *They don't say how they know* → "Where did you first see it fail?"
- *They don't offer an alternative* → "What should people do instead?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

### Q2.2 · ⭐ Where you disagree with peers

**Ask:** "What do you believe about your work that most of your peers would disagree with?"

**Follow up if:**
- *They state the belief without origin* → "What experience led you there?"
- *It sounds sensitive* → "Would you be comfortable saying that publicly?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

---

## Section 3: Recurring Problems

### Q3.1 · ⭐ The most common problem

**Ask:** "What's the problem {{CUSTOMERS}} bring to you more than any other?"

**Follow up if:**
- *They describe it in their own terms* → "How do {{CUSTOMERS}} usually describe it, in their words?"
- *They haven't described their approach* → "What's the first thing you do to diagnose it?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

### Q3.2 · The expensive mistake

**Ask:** "What's a mistake you see {{CUSTOMERS}} make that ends up costing them the most?"

**Follow up if:**
- *They don't name the cost* → "What does it end up costing them: time, money, risk, trust?"
- *They don't offer a fix* → "How would you help them avoid it?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

---

## Section 4: Lessons From Recent Work

### Q4.1 · ⭐ A project that taught you something

**Ask:** "What's a recent project or engagement that taught you something, whether it went better than expected or taught you the hard way?"

**Follow up if:**
- *They don't name the turning point* → "What was the single decision that made the biggest difference?"
- *They haven't reflected* → "What would you do differently if you started it today?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

---

## Section 5: Processes and Frameworks

### Q5.1 · ⭐ How you actually do it

**Ask:** "Walk me through how you approach {{CORE_TASK}}, step by step."

**Follow up if:**
- *They stay high-level* → "What happens in the first step that others tend to skip?"
- *They describe standard steps* → "Where does your approach differ from the textbook version?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

### Q5.2 · Your go-to framework

**Ask:** "Do you have a framework, checklist, or rule of thumb you use over and over?"

**Follow up if:**
- *It's unnamed* → "If you had to name it, what would you call it?"
- *It sounds universal* → "When does it not apply?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

---

## Section 6: Stories

### Q6.1 · ⭐ A story worth telling

**Ask:** "Tell me about a time your work made a real difference for one of your {{CUSTOMERS}}, or a time something went wrong and you learned from it."

**Follow up if:**
- *They skip the before* → "What was the situation before you got involved?"
- *They don't share the outcome* → "What happened in the end?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

---

## Section 7: Questions People Ask

### Q7.1 · The questions you hear most

*Interviewer: collect up to three, one at a time. Ask for one question, then "Another one?" Don't ask for answers unless the SME offers them.*

**Ask:** "What's a question you get from {{CUSTOMERS}} or prospects all the time?"

**Answer:**

| Question they ask | Short answer (optional) |
|---|---|
| | |
| | |
| | |

**Content signal:**

### Q7.2 · The question nobody asks

**Ask:** "What's a question {{CUSTOMERS}} should be asking but almost never do?"

**Follow up if:**
- *They don't answer it* → "How would you answer it?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

---

## Section 8: Predictions

### Q8.1 · ⭐ What's coming

**Ask:** "What will look different in {{INDUSTRY}} in 12 to 24 months, and what should {{AUDIENCE}} do now to get ready?"

**Follow up if:**
- *They're broad* → "What will people stop doing?"
- *They list many actions* → "If someone could do only one thing, which one?"

**Answer:**
>

**Follow-up notes:**
>

**Content signal:**

---

## Optional Modules

*Build Mode adds these when they match the content goals. Each adds about 3 to 5 minutes.*

### Module A: Case Study

**Ask:** "Pick one {{CUSTOMERS}} engagement you're proud of. What was the challenge, what did you do, and what changed?"

**Follow up if:**
- *They skip the result* → "How did you measure success? Any numbers, even rough ones?"
- *They skip the approach* → "What did you do differently than a typical provider would have?"

**Answer:**
>

**Follow-up notes:**
>

### Module B: Technical Deep Dive

**Ask:** "What's a technical concept in your area that's widely misunderstood, even by experienced people? Explain it the way you'd explain it to a peer."

**Follow up if:**
- *They stay abstract* → "Where does that misunderstanding cause real problems?"

**Answer:**
>

**Follow-up notes:**
>

### Module C: Product or Service Perspective

**Ask:** "What problem does {{BRAND_NAME}} solve that buyers tend to underestimate before they see it in action?"

**Follow up if:**
- *It sounds like marketing copy* → "Give me a real moment when one of your {{CUSTOMERS}} realized that."

**Answer:**
>

**Follow-up notes:**
>

### Module D: AI and Technology Shifts

**Ask:** "How is AI changing your work right now, and where should humans stay involved no matter how good the tools get?"

**Follow up if:**
- *They're general* → "Give me one specific task where AI helped, or where it fell short."

**Answer:**
>

**Follow-up notes:**
>

### Module E: Objections and Buying Decisions

**Ask:** "What's the most common objection or hesitation buyers have, and how do you answer it?"

**Follow up if:**
- *They give a sales answer* → "What part of that objection is actually fair?"

**Answer:**
>

**Follow-up notes:**
>

---

## Rapid-Fire Idea Dump

*Interviewer: ask these one at a time, fast. Accept one-line answers and ask no follow-ups. Then ask once: "Anything else rattling around?"*

**Prompts (ask one at a time):**
1. "Something about your work that annoyed you this week?"
2. "One thing you wish all new {{CUSTOMERS}} knew on day one?"
3. "A headline you'd love to see {{BRAND_NAME}} publish?"

**Answers:**
- [ ]
- [ ]
- [ ]
- [ ]

---

## Wrap-Up

*Interviewer: first give the SME a short numbered list of the 6 to 10 strongest ideas from their answers (one line each, with question IDs) so they can react instead of recalling. Then ask the questions below one at a time. Accept answers by number.*

### W1 · Strongest ideas

**Ask:** "Which of these would be most valuable for {{AUDIENCE}}? Pick your top three."

**Answer:**
- [ ]
- [ ]
- [ ]

### W2 · Publishing and flags

**Ask:** "Which are you comfortable seeing published with your name on them? And here's what I flagged for anonymization or fact-checking. Anything to add or remove?" *(List the current `[ANON]`, `[CHECK]`, and `[REMOVE]` flags.)*

**Answer:**

**Comfortable publishing:**
- [ ]
- [ ]
- [ ]

| Idea / Question # | Needs anonymizing? | Needs fact-checking? | Notes |
|---|---|---|---|
| | ☐ | ☐ | |
| | ☐ | ☐ | |

### W3 · Other voices and final thoughts

**Ask:** "Anyone else who could add useful perspective on these? And anything else before we wrap?"

**Answer:**

| Name | Role | Idea they could help with |
|---|---|---|
| | | |
| | | |

**Anything else:**
>

---

# PART 4: AI PROCESSING INSTRUCTIONS

*Run these only after the interview is complete. The SME can ignore this section.*

### Your job

Turn {{SME_NAME}}'s completed interview into a prioritized, production-ready content backlog for {{BRAND_NAME}}. Preserve the SME's actual opinions, stories, and language. Do not flatten distinctive views into safe, generic statements, and do not invent examples, statistics, or {{CUSTOMERS}} details that are not in the answers.

### Context

- **Audience:** {{AUDIENCE}}
- **Content goals:** {{CONTENT_GOALS}}
- **Planned formats:** {{CONTENT_FORMATS}}
- **Priority topics:** {{PRIORITY_TOPICS}}
- **Off-limits:** {{OFF_LIMITS}}
- **Review rules:** {{REVIEW_RULES}}

### Ground rules

1. **Source everything.** Cite the question ID(s) behind every idea, including follow-up notes (for example, `Source: Q2.1, Q6.1 follow-up`).
2. **Use follow-up notes.** They usually hold the most specific material.
3. **Respect flags.** Anonymize anything marked `[ANON]`. Exclude anything marked `[REMOVE]` or covered by the off-limits list. Label anything marked `[CHECK]` as `Needs verification` and never present it as confirmed.
4. **Respect publishing comfort.** Label ideas not selected in W2 as `Confirm with SME before publishing`.
5. **Apply review rules.** Note on each idea which review rules apply.
6. **Skip empty answers.** Do not generate ideas from `[SKIPPED]` or blank responses.
7. **Name gaps honestly.** If an idea is promising but thin, say what additional input is needed.
8. **Respect the audience.** Never frame content in a way that implies the audience lacks expertise.

### Required outputs

#### 1. Categorized content backlog

Group all viable ideas into 4 to 8 categories that reflect the themes in the SME's answers and the priority topics.

#### 2. Content cards

For each idea:

**Working title:** (specific and compelling; no clichés or clickbait)
**Alternate titles:** (2 options with different angles)
**Angle:** (one sentence stating the argument or unique perspective)
**Recommended format:** (from the planned formats, or another format if clearly better)
**Target reader:** (role and situation)
**Search intent and keywords:** (if relevant to the format: intent type plus 1 to 3 keyword phrases)
**Supporting material from the SME:** (specific stories, quotes, frameworks, or data points, with question IDs)
**Evidence status:** (Ready / Needs verification / Needs anonymization / Confirm with SME)
**Review requirements:** (which review rules apply)
**Priority:** (High / Medium / Low)
**Estimated effort:** (Small / Medium / Large)
**Priority rationale:** (one sentence)

#### 3. Priority criteria

Rank using these factors, in order of weight:

1. **Distinctiveness:** An opinion, story, or method competitors couldn't easily replicate
2. **SME ranking:** Selected in W1
3. **Evidence strength:** Backed by specific experience, examples, or results
4. **Goal fit:** Directly supports the content goals and priority topics
5. **Readiness:** Publishable without heavy verification or anonymization

#### 4. Repurposing and split opportunities

- **Split:** For broad ideas, list 2 to 5 focused pieces, each with a one-sentence angle.
- **Repurpose:** For strong ideas, map an anchor piece and its derivatives across the planned formats (for example, an article that becomes a LinkedIn series, a checklist, and a webinar segment).

#### 5. Summary for {{INTERVIEW_OWNER}}

- **Top 5 pieces to produce first**, with one sentence each on why
- **Recurring themes** across multiple answers
- **Follow-up questions for the SME** where a strong idea needs more detail
- **Open items** requiring verification, anonymization, or approval

### Output format

Deliver results in clean Markdown with a heading for each required output, in the order above. Keep content cards scannable and consistent so they can be copied directly into a content calendar or project management tool.

---

*SME Interview Template by [Content Workshop](https://www.contentworkshop.com)*
