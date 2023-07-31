from enum import Enum


class Role(Enum):
    User = 1
    AI = 2


class Message:
    def __init__(self, content: str, role: Role):
        self.content = content
        self.role = role

    def __repr__(self):
        return f'<Role: {self.role}, Content: {self.content}>'


class Chat:
    def __init__(self):
        self._messages = []

    def add_message(self, message: Message):
        self._messages.append(message)

    @property
    def messages(self):
        return self._messages
