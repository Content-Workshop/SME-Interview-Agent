# SME Interview Agent: Requirements

Running list. Add items as we learn them.

| # | Requirement | Source | Status |
|---|---|---|---|
| 1 | **Check ideas against existing posts.** Before the interview, read every post on the brand's site and store a short summary of each. When an answer overlaps a post, ask how the SME's view differs from it. | Test run, 2026-11-17 | In prototype |
| 2 | **Read existing context first.** Load brand materials, past transcripts and earlier interviews before starting, and skip questions they already answer. | Original vision | Proposed |
| 3 | **Ask contextual follow-ups.** Keep the current approach: at most one follow-up per question, using the SME's own words. | Original vision; worked well in the test | Validated |
| 4 | **Store the output.** Save completed interviews and idea banks in a consistent format so they can be reused later. | Original vision | Proposed |
| 5 | **Follow quick mode's follow-up rule.** In the test, the interviewer asked a follow-up on most questions, even though quick mode should skip them unless an answer is under one sentence. | Test run, 2026-11-17 | Proposed |
| 6 | **Voice-to-text answers.** The SME can speak answers that are typed out for them, while the questions stay on screen as text. Include a mic button in the agent's chat interface. | Test feedback, 2026-11-17 | Proposed for v1 |
| 7 | **Anonymization toggle.** The SME can mark client names as anonymized. The internal record keeps the real names for the person receiving the interview. Anything meant for publishing, like drafts and idea cards, shows the anonymized version. | Gap review, 2026-11-17 | Proposed |
| 8 | **Keywords in brand context.** Collect target keywords during onboarding, store them in the brand context, and refresh them periodically. The idea bank uses these keywords instead of making them up. | Gap review, 2026-11-17 | Proposed |
| 9 | **Loadable brands.** Brands can be loaded into the agent, each with its own context: materials, audience, keywords, rules and flags. This includes Content Workshop (with AI Studio as part of it), Chatter as a fully separate brand, and eventually client brands. | Gap review, 2026-11-17 | Proposed |
| 10 | **Reminders.** Send a reminder email if the SME hasn't started the interview, and another if they started but didn't finish. | Gap review, 2026-11-17 | Later version |
| 11 | **Choose interview topics.** The person setting up the interview enters focus topics, and the interviewer leans its questions toward them. The generic template is the default; its questions are tailored to each SME. Later, topics could come from the content calendar. | Prototype build, 2026-11-17 | In prototype |

## Notes

- **#1:** The site's sitemap lists all post URLs (148 at the time of the test). Build the summaries once, then update them as new posts go live.
- **#6:** Voice-to-text is different from full voice interviews. With voice-to-text, only the SME's answers are spoken. In a voice interview, the AI also asks questions out loud and listens, which is a much bigger build.
- **#10:** Moved to a later version. Reminders mean the agent needs the SME's email and has to track each interview's status. That requires a hosted app with accounts. A standalone file can't do it.
- **Open:** test with a busier SME than the first tester, define what success looks like, and decide whether this is standalone or part of Chatter.
- **Later, not v1:** reminders (#10), full voice interviews, and generating interviews from the content calendar.
