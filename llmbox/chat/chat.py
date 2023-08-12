from enum import Enum


class Role(Enum):
    """
    List of roles.
    """
    User = 1
    AI = 2

    def __str__(self):
        return self.name


class PromptFormat(Enum):
    """
    List of prompt formats.
    """
    Anthropic = 1


class Message:
    """
    Class for a message.

    Args:
        text(str): Text of the message
        role(Role): Role of the message
    """

    def __init__(self, text: str, role: Role):
        self.text = text
        self.role = role

    def __repr__(self):
        return f'<Role: {self.role}, Text: {self.text}>'


class Chat:
    """
    Class for a chat session.
    """

    def __init__(self):
        self._messages = []

    def add_message(self, message: Message) -> None:
        """
        Add a message to the chat.

        Args:
            message(Message): Message to be added to chat

        Returns:
            None: None
        """

        self._messages.append(message)

    def generate_prompt(self, prompt_format: PromptFormat) -> str:
        """
        Generate prompt from the chat.

        Args:
            prompt_format(PromptFormat): Format of the prompt

        Returns:
            str: Generated prompt
        """

        if prompt_format == PromptFormat.Anthropic:
            return self.generate_prompt_anthropic()

    def generate_prompt_anthropic(self) -> str:
        """
        Generate prompt from the chat in Anthropic's format.

        Returns:
            str: Generated prompt
        """
        prompt = ''
        for i, message in enumerate(self._messages):
            if i % 2 == 0:
                prompt += f'\n\nHuman: {message.text} \n\nAssistant:'
            else:
                prompt += message.text

        return prompt

    @property
    def messages(self):
        return self._messages

    def __repr__(self):
        return '\n'.join(f'Role: {message.role}\tContent: {message.text}' for message in self._messages)
