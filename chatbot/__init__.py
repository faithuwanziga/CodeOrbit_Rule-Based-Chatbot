"""
Rule-Based Chatbot package.

A simple, transparent chatbot that decides its responses using
predefined rules (regular-expression patterns) instead of machine learning.

Modules
-------
rules.py   : the knowledge base (intents, patterns, responses)
engine.py  : the decision logic (preprocessing, matching, fallback)
cli.py     : the command-line interface used to chat with the bot
"""

from .engine import RuleBasedChatbot, Reply

__all__ = ["RuleBasedChatbot", "Reply"]
__version__ = "1.0.0"
