"""A stand-in for the Anthropic client, used in demo mode and tests.

It returns canned replies so you can click through the app without an API key.
It does not interview anyone for real.
"""

from __future__ import annotations

from types import SimpleNamespace

from agent import FILE_END, FILE_START

DEMO_QUESTIONS = [
    "Welcome! This is demo mode, so the questions are canned.\n\n"
    "**Question 1 of 2**\n\nWhat's something about your work that's been on your mind lately?",
    "**Question 2 of 2**\n\nWhat's a piece of common advice in your field you think is wrong?",
]


class _Block(SimpleNamespace):
    def to_dict(self):
        return dict(self.__dict__)


class _Stream:
    def __init__(self, text: str):
        self._text = text

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    @property
    def text_stream(self):
        for word in self._text.split(" "):
            yield word + " "

    def get_final_message(self):
        return SimpleNamespace(
            content=[_Block(type="text", text=self._text)], stop_reason="end_turn"
        )


class _Messages:
    def __init__(self):
        self.requests: list[dict] = []

    def stream(self, **request):
        self.requests.append(request)
        messages = request["messages"]
        last = messages[-1]["content"]
        if isinstance(last, str) and last.startswith("Completed interview"):
            return _Stream("# Idea Bank (demo)\n\nDemo mode doesn't build real ideas.")
        answers = [m for m in messages[1:] if m["role"] == "user"]
        finished = any(
            isinstance(m["content"], str) and m["content"].strip().lower() == "finish"
            for m in answers
        )
        if finished or len(answers) >= len(DEMO_QUESTIONS):
            recorded = "\n".join(f"> {m['content']}" for m in answers)
            return _Stream(
                f"Thanks, that's everything.\n{FILE_START}\n# Demo Interview\n\n"
                f"**Interview status:** Complete\n\n## Answers\n\n{recorded}\n{FILE_END}"
            )
        return _Stream(DEMO_QUESTIONS[len(answers)])


class DemoClient:
    def __init__(self):
        self.beta = SimpleNamespace(messages=_Messages())
