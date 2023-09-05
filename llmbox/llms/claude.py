from enum import Enum
import os

from anthropic import Anthropic

from .base import BaseLLM, LLMCreator
from ..chat import Chat


class ClaudeModels(Enum):
    """List of Claude LLMs"""

    CLAUDEINSTANT1 = 'claude-instant-1'
    CLAUDE2 = 'claude-2'


class ClaudeInstant1(BaseLLM):
    """
    Class for Claude-Instant-1 LLM by Anthropic.

    Args:
        auth_token(:obj:`str`, optional): Authentication token for Anthropic client.
        api_key(:obj:`str`, optional): API Key for Anthropic client.
        base_url(:obj:`str`, optional): Base URL for Anthropic client.
        timeout(:obj:`float`, optional): Maximum time to connect to Anthropic client.
        max_retries(:obj:`int`, optional): Maximum number of attempts to connect to Anthropic client.

    Example:

        .. code-block:: python

            from llmbox.llms import ClaudeInstant1
            from llmbox.chat import Chat, Message, Role

            llm = ClaudeInstant1()
            chat = Chat()

            chat.add_message(message=Message(text='How big is the earth?', role=Role.User))
            response = llm.generate(chat=chat)
            print(response)

            chat.add_message(message=Message(text=response, role=Role.Assistant))
            chat.add_message(message=Message(text='What about the moon?', role=Role.User))
            next_response = llm.generate(chat=chat)
            print(next_response)
    """

    def __init__(
        self,
        auth_token: str = None,
        api_key: str = None,
        base_url: str = None,
        timeout: float = None,
        max_retries: int = None
    ) -> None:
        # Initialize parent class
        super().__init__(creator=LLMCreator.ANTHROPIC)

        # Verify authentication
        if auth_token is None and api_key is None and os.environ.get('ANTHROPIC_API_KEY') is None:
            raise ValueError('API key not found. '
                             'Set the environment variable ANTHROPIC_API_KEY with your API key (recommended) or '
                             'pass the API key using the `api_key` argument while initializing the class.')

        # Set input arguments
        self._auth_token = auth_token
        self._api_key = api_key
        self._base_url = base_url
        self._timeout = timeout
        self._max_retries = max_retries

        # Create arguments for Anthropic client
        anthropic_arguments = {}
        anthropic_optionals = ['auth_token', 'api_key', 'base_url', 'timeout', 'max_retries']
        for argument in anthropic_optionals:
            if eval(argument) is not None:
                anthropic_arguments[argument] = eval(argument)

        # Initialize Anthropic client
        self._anthropic = Anthropic(**anthropic_arguments)

    def generate(
        self,
        chat: Chat,
        max_tokens: int = 300,
        stop_sequences: list[str] = None,
        temperature: float = None,
        top_p: float = None,
        top_k: int = None
    ) -> str:
        """
        Generate response to a prompt.

        Args:
            chat(Chat): Chat containing the messages.
            max_tokens(:obj:`int`, defaults to 300): Maximum number of tokens to generate before stopping.
            stop_sequences(:obj:`list(str)`, optional): Sequences to stop generating completion text.
            temperature(:obj:`float`, optional): Amount of randomness injected into the response.
            top_p(:obj:`float`, optional): Cutoff probability for nucleus sampling of each subsequent token.
            top_k(:obj:`int`, optional): Number of options to sample from for each subsequent token.

        Returns:
            str: Generated response from the LLM

        Example:

        .. code-block:: python

            from llmbox.llms import ClaudeInstant1
            from llmbox.chat import Chat, Message, Role

            llm = ClaudeInstant1()
            chat = Chat()

            chat.add_message(message=Message(text='How big is the earth?', role=Role.User))
            response = llm.generate(chat=chat)
            print(response)
        """

        # Create arguments for LLM generation
        generation_arguments = {
            'model': 'claude-instant-1',
            'prompt': chat.generate_prompt_anthropic(),
            'max_tokens_to_sample': max_tokens
        }
        generation_optionals = ['stop_sequences', 'temperature', 'top_p', 'top_k']
        for argument in generation_optionals:
            if eval(argument) is not None:
                generation_arguments[argument] = eval(argument)

        # Generate response
        response = self._anthropic.completions.create(**generation_arguments).completion

        return response

    @property
    def base_url(self):
        """str: Base URL for Anthropic client."""

        return self._base_url

    @property
    def timeout(self):
        """float: Maximum time to connect to Anthropic client."""

        return self._timeout

    @property
    def max_retries(self):
        """int: Maximum number of attempts to connect to Anthropic client."""

        return self._max_retries


class Claude2(BaseLLM):
    """
    Class for Claude-2 LLM by Anthropic.

    Args:
        auth_token(:obj:`str`, optional): Authentication token for Anthropic client.
        api_key(:obj:`str`, optional): API Key for Anthropic client.
        base_url(:obj:`str`, optional): Base URL for Anthropic client.
        timeout(:obj:`float`, optional): Maximum time to connect to Anthropic client.
        max_retries(:obj:`int`, optional): Maximum number of attempts to connect to Anthropic client.

    Example:

        .. code-block:: python

            from llmbox.llms import Claude2
            from llmbox.chat import Chat, Message, Role

            llm = Claude2()
            chat = Chat()

            chat.add_message(message=Message(text='How big is the earth?', role=Role.User))
            response = llm.generate(chat=chat)
            print(response)

            chat.add_message(message=Message(text=response, role=Role.Assistant))
            chat.add_message(message=Message(text='What about the moon?', role=Role.User))
            next_response = llm.generate(chat=chat)
            print(next_response)
    """

    def __init__(
        self,
        auth_token: str = None,
        api_key: str = None,
        base_url: str = None,
        timeout: float = None,
        max_retries: int = None
    ) -> None:
        # Initialize parent class
        super().__init__(creator=LLMCreator.ANTHROPIC)

        # Verify authentication
        if auth_token is None and api_key is None and os.environ.get('ANTHROPIC_API_KEY') is None:
            raise ValueError('API key not found. '
                             'Set the environment variable ANTHROPIC_API_KEY with your API key (recommended) or '
                             'pass the API key using the `api_key` argument while initializing the class.')

        # Set input arguments
        self._auth_token = auth_token
        self._api_key = api_key
        self._base_url = base_url
        self._timeout = timeout
        self._max_retries = max_retries

        # Create arguments for Anthropic client
        anthropic_arguments = {}
        anthropic_optionals = ['auth_token', 'api_key', 'base_url', 'timeout', 'max_retries']
        for argument in anthropic_optionals:
            if eval(argument) is not None:
                anthropic_arguments[argument] = eval(argument)

        # Initialize Anthropic client
        self._anthropic = Anthropic(**anthropic_arguments)

    def generate(
        self,
        chat: Chat,
        max_tokens: int = 300,
        stop_sequences: list[str] = None,
        temperature: float = None,
        top_p: float = None,
        top_k: int = None
    ) -> str:
        """
        Generate response to a prompt.

        Args:
            chat(Chat): Chat containing the messages.
            max_tokens(:obj:`int`, defaults to 300): Maximum number of tokens to generate before stopping.
            stop_sequences(:obj:`list(str)`, optional): Sequences to stop generating completion text.
            temperature(:obj:`float`, optional): Amount of randomness injected into the response.
            top_p(:obj:`float`, optional): Cutoff probability for nucleus sampling of each subsequent token.
            top_k(:obj:`int`, optional): Number of options to sample from for each subsequent token.

        Returns:
            str: Generated response from the LLM

        Example:

        .. code-block:: python

            from llmbox.llms import Claude2
            from llmbox.chat import Chat, Message, Role

            llm = Claude2()
            chat = Chat()

            chat.add_message(message=Message(text='How big is the earth?', role=Role.User))
            response = llm.generate(chat=chat)
            print(response)
        """

        # Create arguments for LLM generation
        generation_arguments = {
            'model': 'claude-2',
            'prompt': chat.generate_prompt_anthropic(),
            'max_tokens_to_sample': max_tokens
        }
        generation_optionals = ['stop_sequences', 'temperature', 'top_p', 'top_k']
        for argument in generation_optionals:
            if eval(argument) is not None:
                generation_arguments[argument] = eval(argument)

        # Generate response
        response = self._anthropic.completions.create(**generation_arguments).completion

        return response

    @property
    def base_url(self):
        """str: Base URL for Anthropic client."""

        return self._base_url

    @property
    def timeout(self):
        """float: Maximum time to connect to Anthropic client."""

        return self._timeout

    @property
    def max_retries(self):
        """int: Maximum number of attempts to connect to Anthropic client."""

        return self._max_retries
