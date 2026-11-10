from collections import defaultdict, deque
from time import monotonic

# Spam settings
SPAM_WINDOW = 10
REPEAT_LIMIT = 5
MESSAGE_LIMIT = 12


class SpamFilter:
    def __init__(self):
        # Store recent messages for each user
        self.messages = defaultdict(deque)

    def check_spam(self, guild_id, user_id, content):
        now = monotonic()
        key = (guild_id, user_id)

        history = self.messages[key]

        # Remove messages older than the time window
        while history and now - history[0][0] > SPAM_WINDOW:
            history.popleft()

        # Normalize text for comparison
        normalized = " ".join(content.casefold().split())

        # Record the new message
        history.append((now, normalized))

        # Check repeated messages
        repeat_count = sum(
            1 for _, text in history
            if text == normalized
        )

        if normalized and repeat_count >= REPEAT_LIMIT:
            return "repeated"

        # Check message flooding
        if len(history) >= MESSAGE_LIMIT:
            return "flood"

        return None