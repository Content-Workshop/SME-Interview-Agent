"""Run with:  python -m unittest discover tests"""

import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import agent  # noqa: E402
from agent import FILE_END, FILE_START, GENERIC, Setup  # noqa: E402
from demo_client import DemoClient  # noqa: E402

SETUP = Setup(
    sme_name="Sam",
    sme_role="Content Strategist",
    sme_expertise="AI search, SME interviews",
    core_task="running an SME interview",
    focus_topics="AI search",
)


class BrandTests(unittest.TestCase):
    def test_brands_load(self):
        self.assertEqual(agent.list_brands(), ["chatter", "content-workshop"])
        cw = agent.load_brand("content-workshop")
        self.assertEqual(cw.name, "Content Workshop")
        self.assertEqual(cw.fields["CUSTOMERS"], "clients")
        self.assertIn("ai-studio", cw.templates)
        self.assertTrue(cw.posts.startswith("# Existing Posts"))
        self.assertTrue(cw.past_interviews)

    def test_chatter_is_separate(self):
        chatter = agent.load_brand("chatter")
        self.assertEqual(chatter.name, "Chatter")
        self.assertEqual(chatter.posts, "")
        self.assertNotIn("content-workshop-blog", chatter.templates)


class TemplateTests(unittest.TestCase):
    def test_generic_template_is_filled_and_ready(self):
        brand = agent.load_brand("content-workshop")
        text = agent.template_for(brand, GENERIC, SETUP)
        self.assertNotIn("{{", text)
        self.assertIn("**Template status:** READY", text)
        self.assertNotIn("PART 1: BUILD MODE", text)
        self.assertNotIn("## About This Template", text)
        self.assertIn("# PART 2: INTERVIEW MODE", text)
        self.assertIn("Sam, Content Strategist", text)
        self.assertIn("**Priority topics:** AI search", text)

    def test_brand_template_unchanged(self):
        brand = agent.load_brand("content-workshop")
        text = agent.template_for(brand, "ai-studio", SETUP)
        self.assertEqual(text, brand.templates["ai-studio"])


class PromptTests(unittest.TestCase):
    def test_interview_system_order_and_cache(self):
        brand = agent.load_brand("content-workshop")
        blocks = agent.interview_system(brand, "TEMPLATE")
        self.assertTrue(blocks[0]["text"].startswith("You are running an SME interview"))
        self.assertIn("<existing_posts>", blocks[3]["text"])
        self.assertIn("TEMPLATE", blocks[-1]["text"])
        self.assertEqual(blocks[-1]["cache_control"], {"type": "ephemeral"})
        self.assertEqual(sum("cache_control" in b for b in blocks), 1)

    def test_kickoff_message(self):
        text = agent.kickoff_message(SETUP, today=date(2026, 11, 17))
        self.assertIn("- Interviewee: Sam", text)
        self.assertIn("- Focus topics: AI search", text)
        self.assertIn("- Quick mode: off", text)
        self.assertIn("2026-11-17", text)

    def test_idea_bank_anonymize_toggle(self):
        brand = agent.load_brand("content-workshop")
        on = agent.idea_bank_system(brand, "T", anonymize=True)[0]["text"]
        off = agent.idea_bank_system(brand, "T", anonymize=False)[0]["text"]
        self.assertIn("Replace every name marked [ANON]", on)
        self.assertIn("Keep real names", off)

    def test_request_shape(self):
        client = DemoClient()
        turn = agent.interview_turn(client, [{"type": "text", "text": "s"}], [{"role": "user", "content": "hi"}])
        list(turn.text_stream())
        request = client.beta.messages.requests[-1]
        self.assertEqual(request["model"], "claude-sonnet-5-5")  # the default
        self.assertEqual(request["fallbacks"], "default")
        self.assertEqual(request["betas"], ["server-side-fallback-2026-07-01"])
        self.assertNotIn("thinking", request)

    def test_model_choice(self):
        client = DemoClient()
        for model in agent.MODELS:
            list(agent.interview_turn(client, [], [{"role": "user", "content": "hi"}], model).text_stream())
            request = client.beta.messages.requests[-1]
            self.assertEqual(request["model"], model)
            # Haiku 5.5 has no server-side fallback.
            self.assertEqual("fallbacks" in request, model != "claude-haiku-5-5")


class SplitFileTests(unittest.TestCase):
    def test_split(self):
        text = f"Thanks!\n{FILE_START}\n# File\n\nBody\n{FILE_END}"
        message, file_text = agent.split_interview_file(text)
        self.assertEqual(message, "Thanks!")
        self.assertEqual(file_text, "# File\n\nBody\n")

    def test_split_strips_code_fence(self):
        text = f"{FILE_START}\n```markdown\n# File\n```\n{FILE_END}"
        self.assertEqual(agent.split_interview_file(text)[1], "# File\n")

    def test_no_file(self):
        self.assertEqual(agent.split_interview_file("Question 1?"), ("Question 1?", None))


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.original = agent.OUTPUT_DIR
        agent.OUTPUT_DIR = Path(self.tmp.name)

    def tearDown(self):
        agent.OUTPUT_DIR = self.original
        self.tmp.cleanup()

    def test_full_demo_interview_saves_and_resumes(self):
        brand = agent.load_brand("content-workshop")
        session = agent.new_session("content-workshop", GENERIC, SETUP)
        session.messages.append({"role": "user", "content": agent.kickoff_message(SETUP)})
        system = agent.interview_system(brand, agent.template_for(brand, GENERIC, SETUP))
        client = DemoClient()

        for answer in ["first answer", "second answer", None]:
            turn = agent.interview_turn(client, system, session.messages)
            list(turn.text_stream())
            session.messages.append({"role": "assistant", "content": turn.content})
            session.save()
            if answer:
                session.messages.append({"role": "user", "content": answer})

        _, file_text = agent.split_interview_file(turn.text)
        self.assertIn("second answer", file_text)
        session.save_file("interview.md", file_text)
        session.status = "complete"
        session.save()

        loaded = agent.list_sessions("content-workshop")[0]
        self.assertEqual(loaded.model, agent.DEFAULT_MODEL)
        self.assertEqual(loaded.setup.sme_name, "Sam")
        self.assertEqual(loaded.status, "complete")
        self.assertEqual(len(loaded.messages), len(session.messages))
        # A completed interview becomes context for the next one.
        self.assertTrue(
            any(name.startswith(session.id) for name, _ in agent.load_brand("content-workshop").past_interviews)
        )


if __name__ == "__main__":
    unittest.main()
