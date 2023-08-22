from anthropic import HUMAN_PROMPT, AI_PROMPT
from enum import Enum


class Role(Enum):
    """
    List of roles.
    """

    User = 'user'
    Assistant = 'assistant'

    def __str__(self):
        return self.name


class Message:
    """
    Class for a message.

    Args:
        text(str): Text of the message.
        role(Role): Role of the message.

    Example:

        .. code-block:: python

            from llmbox.chat import Message, Role

            message = Message(text='How big is the earth?', role=Role.User)
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
            message(Message): Message to be added to the chat.

        Returns:
            None: None
        """

        self._messages.append(message)

    def generate_prompt_anthropic(self) -> str:
        """
        Generate prompt from the chat in Anthropic's format.

        Returns:
            str: Prompt string in Anthropic's format.
        """

        prompt = ''
        for i, message in enumerate(self._messages):
            if message.role.value == 'user':
                prompt += f'{HUMAN_PROMPT}: {message.text} {AI_PROMPT}:'
            else:
                prompt += message.text

        return prompt

    def generate_messages_openai(self) -> list[dict]:
        """
        Generate message list from the chat in OpenAI's format.

        Returns:
            list: List of messages in OpenAI's format.
        """

        return [{'role': message.role.value, 'content': message.text} for message in self._messages]

    @property
    def messages(self):
        """
        List of messages in the chat.

        Returns:
            list: List of messages.
        """

        return self._messages

    def __repr__(self):
        return '\n'.join(f'Role: {message.role}\tContent: {message.text}' for message in self._messages)
