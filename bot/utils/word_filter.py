import re
import json
import unicodedata
from pathlib import Path

# File paths
FOLDER = Path(__file__).parent

WORD_FILE = FOLDER / "blocked_words.txt"
JSON_FILE = FOLDER / "leet_dictionary.json"

# Load blocked words
with WORD_FILE.open("r", encoding="utf-8") as file:
    BLOCKED_WORDS = [
        line.strip().lower()
        for line in file
        if line.strip() and not line.startswith("#")
    ]

# Load leetspeak dictionary
with JSON_FILE.open("r", encoding="utf-8") as file:
    LEET_DICTIONARY = json.load(file)


def normalize(text):
    return unicodedata.normalize("NFKC", text).casefold()


def generate_pattern(word):
    parts = []

    for char in normalize(word):
        if char == " ":
            parts.append(r"\s+")
            continue

        # Get substitutions for this letter
        substitutions = LEET_DICTIONARY.get(char.upper(), [])

        # Include original letter and its substitutions
        options = [char] + [
            normalize(sub) for sub in substitutions
        ]

        # Escape special regex characters
        options = [re.escape(option) for option in options]

        # Match any possible substitution
        parts.append(
            "(?:" + "|".join(options) + ")"
        )

    # Allow spaces and punctuation between letters
    pattern = r"[\W_]*".join(parts)

    return re.compile(
        r"(?<!\w)" + pattern + r"(?!\w)",
        re.IGNORECASE
    )


# Generate patterns once when the bot starts
BLOCKED_PATTERNS = [
    generate_pattern(word)
    for word in BLOCKED_WORDS
]


def contains_blocked_word(text):
    normalized = normalize(text)

    for pattern in BLOCKED_PATTERNS:
        if pattern.search(normalized):
            return True

    return False