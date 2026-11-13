# Faith Cafe Chatbot — A Rule-Based Chatbot in Python

| | |
|---|---|
| **Student** | Faith Uwanziga |
| **Course** | Information Management |
| **University** | Adventist University of Central Africa (AUCA) |
| **GitHub repository** | https://github.com/faithuwanziga/CodeOrbit_Rule-Based-Chatbot |

An academic project demonstrating how a chatbot can hold a simple conversation
using **predefined rules and keyword/pattern matching**, without machine learning.

RuleBot acts as the virtual assistant of **Faith Cafe**, a small café in
Kigali, Rwanda. It answers customers' frequently asked questions (menu, prices,
opening hours, location, delivery, payment, reservations, Wi-Fi, contact) and
also handles greetings, small talk and unknown input.

| Business detail | Value |
|---|---|
| Name | Faith Cafe |
| Address | Kigali, Rwanda |
| Phone | 0738 936 166 |
| Email | faithuwanziga5@gmail.com |
| Price | One cup of coffee: 2,500 RWF |

All business information lives in `chatbot/rules.py`, so it can be updated
without changing any program logic.

## Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.10+** | Programming language for the whole project |
| **`re`** (regular expressions) | Pattern matching: recognising keywords in the user's message |
| **`random`** | Choosing a varied reply so the bot sounds less repetitive |
| **`datetime`** | Answering questions about the current time and date |
| **`argparse`** | Command-line options (`--debug`, `--log`) |
| **`unittest`** | Automated testing |
| **Git & GitHub** | Version control and hosting the source code |

No external libraries are required — everything comes with Python.

## 1. Objectives

| Requirement | How it is met |
|---|---|
| Respond to user input using predefined rules/keywords | `chatbot/rules.py` holds 20+ rules, each with regex patterns and replies |
| Handle greetings, questions, and a fallback for unknown input | Greeting, small-talk, FAQ, time/date, math and name rules + a rotating fallback |
| Use Python with if-else or pattern matching logic | Regular-expression matching (`re`), priority selection, if/elif handlers |
| Comments explaining how the bot decides | Every module is documented; `--debug` mode prints the rule that fired |

## 2. Project structure

```
rule_based_chatbot/
├── main.py              # Entry point: python main.py
├── chatbot/
│   ├── __init__.py
│   ├── rules.py         # Knowledge base: intents, patterns, responses, priorities
│   ├── engine.py        # Decision logic: preprocess → match → select → respond
│   └── cli.py           # Command-line interface (debug + logging options)
└── tests/
    └── test_chatbot.py  # 14 unit tests (standard-library unittest)
```

Design principle: **data is separated from logic**. To teach the bot something
new you add a dictionary to `rules.py`; the engine does not change.

## 3. How the chatbot decides its response

```
 User message
      │
      ▼
 1. Validate      empty? → "Please type something…"
      │
      ▼
 2. Preprocess    "Hello!! What's your NAME?" → "hello whats your name"
      │
      ▼
 3. Match         test cleaned text against every rule's regex patterns
      │
      ├── no rule matched ──► 6. Fallback reply (rotating)
      ▼
 4. Select        several matches? → highest priority wins (ties: first listed)
      │
      ▼
 5. Respond       handler? → dynamic reply (name, time, math)
                  otherwise → random reply from the rule's list
```

**Why priorities?** A message can match more than one rule.
`"thanks, bye!"` matches both *thanks* (priority 45) and *goodbye* (priority 100);
goodbye wins, so the conversation ends correctly. Similarly,
`"what time do you open?"` matches both the clock-*time* rule (70) and the
*opening hours* rule (72); the business answer wins, as the customer intended.

**Why word boundaries (`\b`)?** Without them, `hi` would match inside `this`,
producing false greetings. A unit test checks this.

## 4. Features

- **Business FAQ for Faith Cafe:** menu, prices (RWF), opening hours, location,
  delivery and takeaway, payment (cash, MTN MoMo, Airtel Money, card),
  orders and table reservations, Wi-Fi, contact details
- Greetings (personalised once the bot knows your name)
- Small talk: how are you, bot identity, creator, jokes, thanks
- **Memory:** "My name is Alex" → "What is my name?" → "Your name is Alex."
- **Dynamic answers:** current time and date
- **Arithmetic:** e.g. adding up a bill — "what is 1500 plus 3500" (division-by-zero safe)
- Fallback that rotates its wording and suggests typing `help`
- `--debug` flag showing the matched intent and pattern (useful in a presentation)
- `--log FILE` flag to save the conversation transcript

## 5. Setup Instructions

**Requirement:** Python 3.10 or newer ([download Python](https://www.python.org/downloads/)).
Check your version with `python --version` (on some systems: `python3 --version`).
No other installation is needed.

**Step 1 — Get the code**

```bash
git clone https://github.com/faithuwanziga/CodeOrbit_Rule-Based-Chatbot.git
cd CodeOrbit_Rule-Based-Chatbot
```

Or click **Code → Download ZIP** on the GitHub page, unzip it, and open a
terminal in the unzipped folder.

**Step 2 — Run the chatbot**

```bash
python main.py                    # chat normally
python main.py --debug            # also show which rule answered and why
python main.py --log chat.txt     # save the conversation to chat.txt
```

Type `help` to see what the bot can do, and `bye` to exit.

**Step 3 — Run the tests (optional)**

```bash
python -m unittest discover -s tests -v
```

### Sample session (`--debug`)

```
You: hello
RuleBot: Hi there! Ask me about our menu, prices, hours or delivery.
   [intent=greeting | pattern=^(hi|hello|hey|hiya|howdy|greetings|yo)\b]
You: my name is faith
RuleBot: Nice to meet you, Faith! I'll remember your name.
   [intent=set_name | pattern=\bmy name is ([a-z]+)\b]
You: what is on the menu
RuleBot: At Faith Cafe we serve freshly made coffee (2,500 RWF a cup),
         along with tea, juices and snacks. Ask me about prices!
   [intent=faq_menu]
You: how much is a cup of coffee
RuleBot: One cup of coffee costs 2,500 RWF. For the prices of other items,
         please ask our staff or call 0738 936 166.
   [intent=faq_prices]
You: how can i contact you
RuleBot: You can contact Faith Cafe by phone on 0738 936 166
         or by email at faithuwanziga5@gmail.com.
   [intent=faq_contact]
You: can i pay with momo
RuleBot: We accept cash, MTN Mobile Money, Airtel Money and bank cards.
   [intent=faq_payment]
You: what is 1500 plus 3500
RuleBot: The answer is 5000.
   [intent=math]
You: this is strange
RuleBot: Sorry, I didn't understand that. Could you rephrase?
   [intent=fallback | pattern=-]
You: thanks, bye
RuleBot: Goodbye! Have a great day.
   [intent=goodbye]
```

## 6. Testing

15 automated tests cover preprocessing, intent recognition, all nine business
FAQ intents, word boundaries, fallback rotation, empty input, priority
conflicts, name memory, arithmetic (including divide-by-zero), conversation
history and knowledge-base validation.

```
Ran 15 tests in 0.004s
OK
```

During development, the tests revealed a real rule conflict: "What time do you
open?" was first answered with the current clock time. Raising the priority of
the opening-hours rule fixed it — a good example of why rule-based systems need
testing and careful priority design.

## 7. Adding a new rule

```python
# in chatbot/rules.py, inside RULES
{
    "intent": "faq_parking",
    "priority": 60,
    "patterns": [r"\b(parking|park my car|where can i park)\b"],
    "responses": ["Free parking is available in front of Faith Cafe."],
},
```

## 8. Limitations (for discussion in the report)

- Understands only phrasings anticipated by its patterns; synonyms or typos
  outside the rules fall through to the fallback.
- No real context beyond the remembered name — each message is handled mostly
  independently.
- The knowledge base grows manually; large rule sets become hard to maintain
  and rules may conflict (mitigated here by priorities).

## 9. Possible extensions

- Fuzzy matching (`difflib`) to tolerate spelling mistakes
- Load rules from a JSON file so non-programmers can edit them
- A web or GUI front end (Flask, Tkinter)
- Compare against an ML intent classifier (e.g. scikit-learn) as future work
