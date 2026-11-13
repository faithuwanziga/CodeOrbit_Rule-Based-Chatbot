"""
cli.py — Command-line interface for RuleBot.

Usage:
    python main.py            # normal chat
    python main.py --debug    # also show WHICH rule fired and WHY
    python main.py --log chat_log.txt   # save the conversation to a file
"""

import argparse
from datetime import datetime

from .engine import RuleBasedChatbot


def run(debug: bool = False, log_path: str | None = None) -> None:
    bot = RuleBasedChatbot()
    print("=" * 60)
    print(f"  {bot.name} - Faith Cafe virtual assistant (rule-based chatbot)")
    print("  By Faith Uwanziga | Information Management, AUCA")
    print("  Type 'help' for options, 'bye' to exit.")
    print("=" * 60)

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):  # Ctrl+D / Ctrl+C exits cleanly
            print(f"\n{bot.name}: Goodbye!")
            break

        reply = bot.respond(user_input)
        print(f"{bot.name}: {reply.text}")

        # Debug mode makes the decision process visible (great for demos).
        if debug:
            print(f"   [intent={reply.intent} | pattern={reply.matched_pattern or '-'}]")

        if reply.end_conversation:
            break

    if log_path:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"Chat log - {datetime.now():%Y-%m-%d %H:%M}\n\n")
            for message, r in bot.history:
                f.write(f"You: {message}\n{bot.name}: {r.text}  [intent={r.intent}]\n")
        print(f"(Conversation saved to {log_path})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the rule-based chatbot.")
    parser.add_argument("--debug", action="store_true", help="show matched intent and pattern")
    parser.add_argument("--log", metavar="FILE", help="save the conversation to FILE")
    args = parser.parse_args()
    run(debug=args.debug, log_path=args.log)
