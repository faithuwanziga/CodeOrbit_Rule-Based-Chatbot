"""
engine.py — The chatbot's DECISION LOGIC.

Author : Faith Uwanziga
Course : Information Management, Adventist University of Central Africa (AUCA)

How the chatbot decides its response (the pipeline)
---------------------------------------------------
For every message the user types, `RuleBasedChatbot.respond()` runs:

    1. VALIDATE    Empty input?  -> ask the user to type something.
    2. PREPROCESS  Normalise the text: lower-case, remove punctuation,
                   collapse spaces ("Hello!!  How ARE you?" -> "hello how are you").
    3. MATCH       Test the cleaned text against the regex patterns of every
                   rule in rules.py and collect all rules that match.
    4. SELECT      If several rules match, choose the one with the highest
                   priority (ties: the rule listed first in rules.py wins).
    5. RESPOND     If the chosen rule has a handler, call it to build a dynamic
                   reply; otherwise pick a random reply from its responses.
    6. FALLBACK    If NO rule matched, return a fallback reply.

Every exchange is also recorded in `self.history`, which is useful for
debugging, evaluation and for the project report.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from datetime import datetime

from .rules import FALLBACK_RESPONSES, RULES


@dataclass
class Reply:
    """The result of one decision: the text plus *why* it was chosen."""

    text: str
    intent: str          # the rule that fired, or "fallback"
    matched_pattern: str  # the regex that matched ("" for fallback/empty)
    end_conversation: bool = False


class RuleBasedChatbot:
    """A transparent chatbot that maps user input to replies using rules."""

    def __init__(self, rules=None, fallback_responses=None, name="RuleBot", seed=None):
        self.name = name
        self.rules = rules if rules is not None else RULES
        self.fallback_responses = fallback_responses or FALLBACK_RESPONSES
        self._fallback_index = 0
        self._random = random.Random(seed)  # a seed makes replies reproducible (tests)
        self.user_name: str | None = None   # simple memory
        self.history: list[tuple[str, Reply]] = []

        # Pre-compile every pattern once at start-up (faster than compiling
        # on every message) and validate the knowledge base early.
        self._compiled = []
        for order, rule in enumerate(self.rules):
            if "responses" not in rule and "handler" not in rule:
                raise ValueError(f"Rule '{rule['intent']}' needs 'responses' or 'handler'.")
            patterns = [re.compile(p) for p in rule["patterns"]]
            self._compiled.append((order, rule, patterns))

    # ------------------------------------------------------------------ #
    # Step 2: preprocessing
    # ------------------------------------------------------------------ #
    @staticmethod
    def preprocess(message: str) -> str:
        """Normalise text so that small differences don't break matching.

        - lower-case everything            ("HeLLo" -> "hello")
        - turn apostrophes into spaces     ("what's" -> "what s" -> handled below)
        - keep letters, digits, spaces and the math symbols + - * / .
        - collapse repeated whitespace
        """
        text = message.lower().strip()
        text = text.replace("what's", "whats").replace("today's", "todays").replace("how's", "hows")
        text = re.sub(r"['’]", " ", text)             # "i'm" -> "i m"
        text = re.sub(r"[^a-z0-9\s+\-*/.]", " ", text)  # drop other punctuation
        text = re.sub(r"(?<!\d)\.|\.(?!\d)", " ", text)  # keep '.' only inside numbers (3.5)
        return re.sub(r"\s+", " ", text).strip()

    # ------------------------------------------------------------------ #
    # Steps 3-4: matching and selection
    # ------------------------------------------------------------------ #
    def match(self, cleaned: str):
        """Return (rule, regex_match) for the best rule, or (None, None).

        Every rule is tested. Among the rules that match, the highest
        `priority` wins; for equal priority the earlier rule wins.
        """
        candidates = []
        for order, rule, patterns in self._compiled:
            for pattern in patterns:
                found = pattern.search(cleaned)
                if found:
                    # Sort key: higher priority first, then earlier position.
                    candidates.append((-rule.get("priority", 0), order, rule, found))
                    break  # one matching pattern is enough for this rule
        if not candidates:
            return None, None
        candidates.sort(key=lambda c: (c[0], c[1]))
        _, _, rule, found = candidates[0]
        return rule, found

    # ------------------------------------------------------------------ #
    # Steps 1-6: the full pipeline
    # ------------------------------------------------------------------ #
    def respond(self, message: str) -> Reply:
        """Decide and return the bot's reply to one user message."""
        # Step 1: validate
        if not message or not message.strip():
            reply = Reply("Please type something so I can help you.", "empty_input", "")
            self.history.append((message, reply))
            return reply

        # Step 2: preprocess
        cleaned = self.preprocess(message)

        # Steps 3-4: match and select
        rule, found = self.match(cleaned)

        if rule is None:
            # Step 6: fallback — rotate so consecutive misses get different replies
            text = self.fallback_responses[self._fallback_index % len(self.fallback_responses)]
            self._fallback_index += 1
            reply = Reply(text, "fallback", "")
        else:
            # Step 5: build the response (dynamic handler or static list)
            if "handler" in rule:
                handler = getattr(self, rule["handler"])
                text = handler(found)
            else:
                text = self._random.choice(rule["responses"])
            reply = Reply(
                text=text,
                intent=rule["intent"],
                matched_pattern=found.re.pattern,
                end_conversation=(rule["intent"] == "goodbye"),
            )

        self.history.append((message, reply))
        return reply

    # ------------------------------------------------------------------ #
    # Handlers: functions that build DYNAMIC replies.
    # Each receives the regex match object, so it can read captured groups.
    # ------------------------------------------------------------------ #
    def handle_greeting(self, found) -> str:
        if self.user_name:
            return f"Hello again, {self.user_name}! How can I help you?"
        return self._random.choice([
            "Hello! Welcome to Faith Cafe. How can I help you today?",
            "Hi there! Ask me about our menu, prices, hours or delivery.",
            "Hey! Welcome to Faith Cafe. What's your name?",
        ])

    def handle_set_name(self, found) -> str:
        self.user_name = found.group(1).capitalize()  # group(1) = captured name
        return f"Nice to meet you, {self.user_name}! I'll remember your name."

    def handle_get_user_name(self, found) -> str:
        if self.user_name:
            return f"Your name is {self.user_name}."
        return "I don't know your name yet. You can tell me by saying 'My name is ...'."

    def handle_time(self, found) -> str:
        return f"The current time is {datetime.now().strftime('%H:%M')}."

    def handle_date(self, found) -> str:
        return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."

    def handle_math(self, found) -> str:
        a, op, b = float(found.group(1)), found.group(2), float(found.group(3))
        if op in ("plus", "+"):
            result = a + b
        elif op in ("minus", "-"):
            result = a - b
        elif op in ("times", "multiplied by", "x", "*"):
            result = a * b
        else:  # division
            if b == 0:
                return "I can't divide by zero!"
            result = a / b
        result = int(result) if float(result).is_integer() else round(result, 4)
        return f"The answer is {result}."

    def handle_help(self, found) -> str:
        return (
            "Here's what I can do:\n"
            "  - Answer questions about Faith Cafe: menu, prices, opening hours,\n"
            "    location, delivery, payment, orders and reservations, Wi-Fi, contact\n"
            "  - Greet you and make small talk (try 'hello', 'how are you?')\n"
            "  - Remember your name ('my name is Alex', 'what is my name?')\n"
            "  - Tell the time or date ('what time is it?')\n"
            "  - Do simple math, e.g. to add up a bill ('what is 1500 plus 3500?')\n"
            "  - Tell a joke ('tell me a joke')\n"
            "  - Say 'bye' to end the chat"
        )
