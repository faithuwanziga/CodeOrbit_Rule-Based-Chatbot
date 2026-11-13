"""
rules.py — The chatbot's KNOWLEDGE BASE.

Author : Faith Uwanziga
Course : Information Management, Adventist University of Central Africa (AUCA)

How the chatbot "knows" things
------------------------------
A rule-based chatbot has no learning. Everything it can understand is written
here by hand as a list of RULES. Each rule describes one INTENT (what the user
wants) and contains:

    intent    : a unique name for the rule, e.g. "greeting"
    patterns  : regular expressions (regex). If ANY pattern is found in the
                user's cleaned message, the rule "fires".
    responses : possible replies. One is chosen at random so the bot
                sounds less robotic.
    priority  : a number. When several rules match the same message, the
                rule with the HIGHEST priority wins. This resolves conflicts,
                e.g. "bye, thanks" matches both "thanks" and "goodbye", but
                goodbye has higher priority so the conversation ends.
    handler   : (optional) the name of a function in engine.py that builds a
                DYNAMIC reply (current time, a remembered name, arithmetic...).
                If a handler is given, it is used instead of `responses`.

Pattern notes
-------------
* Messages are lower-cased and stripped of most punctuation BEFORE matching,
  so patterns are written in lower case.
* `\\b` means "word boundary" so that "hi" matches "hi there" but NOT "this".
* Rules are plain data: to teach the bot something new you only add a
  dictionary to RULES — no change to the engine is needed.
"""

RULES = [
    # ------------------------------------------------------------------ #
    # 1. Conversation control
    # ------------------------------------------------------------------ #
    {
        "intent": "goodbye",
        "priority": 100,  # highest: an exit request always wins
        "patterns": [
            r"\b(bye|goodbye|good bye|see you|see ya|farewell|exit|quit)\b",
            r"\b(good night|gotta go|i have to go|talk later)\b",
        ],
        "responses": [
            "Goodbye! Have a great day.",
            "See you later! Thanks for chatting.",
            "Bye! Come back any time.",
        ],
    },
    {
        "intent": "help",
        "priority": 90,
        # "menu" is NOT a help keyword here, because customers ask for the cafe menu.
        "patterns": [r"\b(help|what can you do|commands|options)\b"],
        "handler": "handle_help",
    },

    # ------------------------------------------------------------------ #
    # 2. Personal memory (the bot remembers the user's name)
    # ------------------------------------------------------------------ #
    {
        "intent": "set_name",
        "priority": 80,
        # The ( ) group CAPTURES the name so the handler can store it.
        "patterns": [
            r"\bmy name is ([a-z]+)\b",
            r"\bcall me ([a-z]+)\b",
            r"^i am ([a-z]+)$",
            r"^i m ([a-z]+)$",
        ],
        "handler": "handle_set_name",
    },
    {
        "intent": "get_user_name",
        "priority": 80,
        "patterns": [r"\b(what is|whats|do you know|do you remember) my name\b"],
        "handler": "handle_get_user_name",
    },

    # ------------------------------------------------------------------ #
    # 3. Dynamic information
    # ------------------------------------------------------------------ #
    {
        "intent": "time",
        "priority": 70,
        "patterns": [r"\b(what time|the time|current time|time is it)\b"],
        "handler": "handle_time",
    },
    {
        "intent": "date",
        "priority": 70,
        "patterns": [r"\b(what day|the date|todays date|what is today|which day)\b"],
        "handler": "handle_date",
    },
    {
        "intent": "math",
        "priority": 75,
        # Captures: number, operator word/symbol, number. e.g. "what is 4 plus 5"
        "patterns": [
            r"(-?\d+(?:\.\d+)?)\s*(plus|minus|times|multiplied by|divided by|\+|-|x|\*|/)\s*(-?\d+(?:\.\d+)?)"
        ],
        "handler": "handle_math",
    },

    # ------------------------------------------------------------------ #
    # 4. Greetings and small talk
    # ------------------------------------------------------------------ #
    {
        "intent": "greeting",
        "priority": 50,
        "patterns": [
            r"^(hi|hello|hey|hiya|howdy|greetings|yo)\b",
            r"\bgood (morning|afternoon|evening)\b",
        ],
        "handler": "handle_greeting",  # greets by name if known
    },
    {
        "intent": "how_are_you",
        "priority": 55,
        "patterns": [r"\bhow (are|r) (you|u)\b", r"\bhow is it going\b", r"\bhows it going\b"],
        "responses": [
            "I'm just a program, but I'm running perfectly! How about you?",
            "Doing great, thanks for asking! How are you?",
        ],
    },
    {
        "intent": "user_feels_good",
        "priority": 40,
        "patterns": [r"\bi m (fine|good|great|well|ok|okay)\b", r"\bi am (fine|good|great|well|ok|okay)\b"],
        "responses": ["Glad to hear that!", "Awesome! What can I do for you?"],
    },
    {
        "intent": "user_feels_bad",
        "priority": 40,
        "patterns": [r"\bi m (sad|tired|bad|not ok|stressed)\b", r"\bi am (sad|tired|bad|not ok|stressed)\b"],
        "responses": [
            "I'm sorry to hear that. Taking a short break or talking to a friend can help.",
            "That sounds tough. I'm here if you want to chat.",
        ],
    },
    {
        "intent": "bot_name",
        "priority": 60,
        "patterns": [r"\b(what is|whats) your name\b", r"\bwho are you\b"],
        "responses": [
            "I'm RuleBot, the virtual assistant of Faith Cafe.",
            "My name is RuleBot. I answer questions about Faith Cafe using predefined rules.",
        ],
    },
    {
        "intent": "bot_creator",
        "priority": 60,
        "patterns": [r"\bwho (made|created|built|programmed) you\b"],
        "responses": [
            "I was built by Faith Uwanziga as an academic project for the Information "
            "Management course at the Adventist University of Central Africa."
        ],
    },
    {
        "intent": "how_work",
        "priority": 60,
        "patterns": [r"\bhow do you work\b", r"\bare you (an )?(ai|robot|bot|human)\b"],
        "responses": [
            "I'm a rule-based bot: I clean your message, compare it against keyword "
            "patterns, and reply with the answer linked to the best-matching rule."
        ],
    },
    {
        "intent": "thanks",
        "priority": 45,
        "patterns": [r"\b(thanks|thank you|thx|appreciate it)\b"],
        "responses": ["You're welcome!", "Happy to help!", "Any time!"],
    },
    {
        "intent": "joke",
        "priority": 60,
        "patterns": [r"\b(joke|make me laugh|something funny)\b"],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "There are 10 types of people: those who understand binary and those who don't.",
            "Why did the developer go broke? Because he used up all his cache.",
        ],
    },

    # ------------------------------------------------------------------ #
    # 5. Small-business FAQ: "Faith Cafe", Kigali, Rwanda.
    #    All details below are confirmed by the owner: name, address, phone,
    #    email, coffee price (2,500 RWF per cup), opening hours, menu,
    #    payment methods, takeaway/delivery and free Wi-Fi.
    #    To update the business information, edit only the responses here.
    # ------------------------------------------------------------------ #
    {
        "intent": "faq_hours",
        # 72 > 70 (the "time" rule): "what time do you open?" asks about opening
        # hours, not the current clock time, so this rule must win the conflict.
        "priority": 72,
        "patterns": [
            r"\b(opening hours|working hours|business hours|closing time)\b",
            r"\b(are you|is the cafe|when do you|what time do you) (open|close)\b",
            r"\bopen (today|on|at)\b",
        ],
        "responses": [
            "Faith Cafe is open Monday to Saturday from 7:00 to 21:00, "
            "and on Sunday from 9:00 to 18:00."
        ],
    },
    {
        "intent": "faq_location",
        "priority": 60,
        "patterns": [r"\b(where are you|location|address|located|directions|find you)\b"],
        "responses": [
            "Faith Cafe is located in Kigali, Rwanda. Call us on 0738 936 166 for directions."
        ],
    },
    {
        "intent": "faq_menu",
        "priority": 60,
        "patterns": [r"\b(menu|what do you (sell|serve|have)|food|drinks|coffee|tea|breakfast|lunch)\b"],
        "responses": [
            "At Faith Cafe we serve freshly made coffee (2,500 RWF a cup), "
            "along with tea, juices and snacks. Ask me about prices!"
        ],
    },
    {
        "intent": "faq_prices",
        "priority": 65,
        "patterns": [r"\b(price|prices|cost|how much|expensive|cheap)\b"],
        "responses": [
            "One cup of coffee costs 2,500 RWF. For the prices of other items, "
            "please ask our staff or call 0738 936 166."
        ],
    },
    {
        "intent": "faq_delivery",
        "priority": 62,
        "patterns": [r"\b(deliver|delivery|take away|takeaway|take out)\b"],
        "responses": [
            "Yes! We offer takeaway. For delivery within Kigali, "
            "call us on 0738 936 166 to place your order."
        ],
    },
    {
        "intent": "faq_payment",
        "priority": 62,
        "patterns": [r"\b(pay|payment|momo|mobile money|airtel money|card|cash)\b"],
        "responses": ["We accept cash, MTN Mobile Money, Airtel Money and bank cards."],
    },
    {
        "intent": "faq_order",
        "priority": 61,
        "patterns": [r"\b(order|reserve|reservation|book a table|booking)\b"],
        "responses": [
            "You can order at the counter, or call us to order ahead or reserve a table."
        ],
    },
    {
        "intent": "faq_wifi",
        "priority": 60,
        "patterns": [r"\b(wifi|wi fi|internet)\b"],
        "responses": ["Yes, we have free Wi-Fi for customers. Ask the staff for the password."],
    },
    {
        "intent": "faq_contact",
        "priority": 60,
        "patterns": [r"\b(contact|email|phone|call you|reach you|phone number)\b"],
        "responses": [
            "You can contact Faith Cafe by phone on 0738 936 166 "
            "or by email at faithuwanziga5@gmail.com."
        ],
    },
    {
        "intent": "faq_chatbot",
        "priority": 60,
        "patterns": [r"\bwhat is a (rule based )?chatbot\b"],
        "responses": [
            "A chatbot is a program that converses with users. A rule-based chatbot "
            "follows hand-written rules instead of learning from data."
        ],
    },
]

# Replies used when NO rule matches (the fallback). The engine rotates through
# them in order so the user does not see the same sentence twice in a row.
FALLBACK_RESPONSES = [
    "Sorry, I didn't understand that. Could you rephrase?",
    "I'm not sure how to answer that yet. Type 'help' to see what I can do.",
    "Hmm, that's outside my rules. Try asking something else!",
]
