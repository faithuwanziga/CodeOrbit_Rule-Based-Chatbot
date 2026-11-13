"""
Unit tests for RuleBot. Uses only the standard library (unittest).

Run from the project folder:
    python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot import RuleBasedChatbot  # noqa: E402


class TestPreprocessing(unittest.TestCase):
    def test_lowercase_and_punctuation(self):
        self.assertEqual(RuleBasedChatbot.preprocess("  HeLLo!!  There?? "), "hello there")

    def test_contractions(self):
        self.assertEqual(RuleBasedChatbot.preprocess("I'm fine"), "i m fine")
        self.assertEqual(RuleBasedChatbot.preprocess("What's your name?"), "whats your name")

    def test_keeps_decimal_numbers(self):
        self.assertEqual(RuleBasedChatbot.preprocess("2.5 plus 1."), "2.5 plus 1")


class TestIntents(unittest.TestCase):
    def setUp(self):
        self.bot = RuleBasedChatbot(seed=42)

    def assertIntent(self, message, intent):
        self.assertEqual(self.bot.respond(message).intent, intent, msg=message)

    def test_greetings(self):
        for msg in ["Hello", "hi there", "Hey!", "Good morning"]:
            self.assertIntent(msg, "greeting")

    def test_word_boundaries(self):
        # "this" contains "hi" but must NOT be treated as a greeting
        self.assertNotEqual(self.bot.respond("this is strange").intent, "greeting")

    def test_questions(self):
        self.assertIntent("How are you?", "how_are_you")
        self.assertIntent("What's your name?", "bot_name")
        self.assertIntent("Tell me a joke", "joke")
        self.assertIntent("What time is it?", "time")

    def test_business_faq(self):
        self.assertIntent("What time do you open?", "faq_hours")
        self.assertIntent("Can I see the menu?", "faq_menu")
        self.assertIntent("How much is a coffee?", "faq_prices")
        self.assertIntent("Do you deliver?", "faq_delivery")
        self.assertIntent("Can I pay with MoMo?", "faq_payment")
        self.assertIntent("Where are you located?", "faq_location")
        self.assertIntent("I want to book a table", "faq_order")
        self.assertIntent("Do you have wifi?", "faq_wifi")
        self.assertIntent("What is your phone number?", "faq_contact")

    def test_fallback(self):
        reply = self.bot.respond("xyzzy quantum banana")
        self.assertEqual(reply.intent, "fallback")

    def test_fallback_rotates(self):
        first = self.bot.respond("asdf").text
        second = self.bot.respond("qwer").text
        self.assertNotEqual(first, second)

    def test_empty_input(self):
        self.assertEqual(self.bot.respond("   ").intent, "empty_input")

    def test_priority_goodbye_beats_thanks(self):
        reply = self.bot.respond("thanks, bye!")
        self.assertEqual(reply.intent, "goodbye")
        self.assertTrue(reply.end_conversation)


class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.bot = RuleBasedChatbot(seed=1)

    def test_name_memory(self):
        self.assertIn("don't know", self.bot.respond("what is my name?").text)
        self.bot.respond("My name is alice")
        self.assertEqual(self.bot.user_name, "Alice")
        self.assertIn("Alice", self.bot.respond("what is my name").text)
        self.assertIn("Alice", self.bot.respond("hello").text)

    def test_math(self):
        self.assertEqual(self.bot.respond("what is 12 times 4?").text, "The answer is 48.")
        self.assertEqual(self.bot.respond("7 + 3").text, "The answer is 10.")
        self.assertEqual(self.bot.respond("10 divided by 4").text, "The answer is 2.5.")
        self.assertEqual(self.bot.respond("5 / 0").text, "I can't divide by zero!")

    def test_history_recorded(self):
        self.bot.respond("hi")
        self.bot.respond("bye")
        self.assertEqual(len(self.bot.history), 2)


class TestKnowledgeBaseValidation(unittest.TestCase):
    def test_rule_without_reply_rejected(self):
        bad_rules = [{"intent": "broken", "patterns": [r"x"]}]
        with self.assertRaises(ValueError):
            RuleBasedChatbot(rules=bad_rules)


if __name__ == "__main__":
    unittest.main()
