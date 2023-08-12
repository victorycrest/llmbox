from enum import Enum


class Role(Enum):
    User = 1
    AI = 2

    def __str__(self):
        return self.name


class PromptFormat(Enum):
    Anthropic = 1


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

    def generate_prompt(self, prompt_format: PromptFormat):
        if prompt_format == PromptFormat.Anthropic:
            return self.generate_prompt_anthropic()

    def generate_prompt_anthropic(self):
        prompt = ''
        for i, message in enumerate(self._messages):
            if i % 2 == 0:
                prompt += f'\n\nHuman: {message.content} \n\nAssistant:'
            else:
                prompt += message.content

        return prompt

    @property
    def messages(self):
        return self._messages

    def __repr__(self):
        return '\n'.join(f'Role: {message.role}\tContent: {message.content}' for message in self._messages)
