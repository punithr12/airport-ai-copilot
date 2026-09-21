class ConversationMemory:

    def __init__(self, max_messages=10):
        self.history = []
        self.max_messages = max_messages

    def add_message(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })

        # Keep only recent conversation
        if len(self.history) > self.max_messages:
            self.history = self.history[
                -self.max_messages:
            ]

    def get_history(self):
        return self.history

    def get_context(self):
        if not self.history:
            return ""

        lines = []

        for message in self.history:
            lines.append(
                f"{message['role']}: {message['content']}"
            )

        return "\n".join(lines)

    def clear(self):
        self.history = []