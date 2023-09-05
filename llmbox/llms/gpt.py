from enum import Enum
import os

import openai

from .base import BaseLLM, LLMCreator
from ..chat import Chat


class GPTModels(Enum):
    """List of GPT LLMs"""

    GPT35TURBO = 'gpt-3.5-turbo'
    GPT4 = 'gpt-4'


class GPT35Turbo(BaseLLM):
    """
    Class for GPT-3.5-Turbo LLM by OpenAI.

    Args:
        api_key(:obj:`str`, optional): API Key for OpenAI client.

    Example:

        .. code-block:: python

            from llmbox.llms import GPT35Turbo
            from llmbox.chat import Chat, Message, Role

            llm = GPT35Turbo()
            chat = Chat()

            chat.add_message(message=Message(text='How big is the earth?', role=Role.User))
            response = llm.generate(chat=chat)
            print(response)

            chat.add_message(message=Message(text=response, role=Role.Assistant))
            chat.add_message(message=Message(text='What about the moon?', role=Role.User))
            next_response = llm.generate(chat=chat)
            print(next_response)
    """

    def __init__(self, api_key: str = None) -> None:
        # Initialize parent class
        super().__init__(creator=LLMCreator.OPENAI)

        # Verify authentication
        if api_key is None and os.environ.get('OPENAI_API_KEY') is None:
            raise ValueError('API key not found. '
                             'Set the environment variable OPENAI_API_KEY with your API key (recommended) or '
                             'pass the API key using the `api_key` argument while initializing the class.')

        # Initialize OpenAI client
        self._openai = openai
        if api_key is not None:
            self._openai.api_key = api_key
        else:
            self._openai.api_key = os.environ['OPENAI_API_KEY']

    def generate(
            self,
            chat: Chat,
            max_tokens: int = None,
            stop_sequences: list[str] = None,
            temperature: float = None,
            top_p: float = None
    ) -> str:
        """
        Generate response to a prompt.

        Args:
            chat(Chat): Chat containing the messages.
            max_tokens(:obj:`int`, optional): Maximum number of tokens to generate before stopping.
            stop_sequences(:obj:`list(str)`, optional): Sequences to stop generating completion text.
            temperature(:obj:`float`, optional): Amount of randomness injected into the response.
            top_p(:obj:`float`, optional): Cutoff probability for nucleus sampling of each subsequent token.

        Returns:
            str: Generated response from the LLM

        Example:

        .. code-block:: python

            from llmbox.llms import GPT35Turbo
            from llmbox.chat import Chat, Message, Role

            llm = GPT35Turbo()
            chat = Chat()

            chat.add_message(message=Message(text='How big is the earth?', role=Role.User))
            response = llm.generate(chat=chat)
            print(response)
        """

        # Create arguments for LLM generation
        generation_arguments = {
            'model': 'gpt-3.5-turbo',
            'messages': chat.generate_messages_openai()
        }
        generation_optionals = ['max_tokens', 'stop_sequences', 'temperature', 'top_p']
        for argument in generation_optionals:
            if eval(argument) is not None:
                generation_arguments[argument] = eval(argument)

        # Generate response
        response = openai.ChatCompletion.create(**generation_arguments).choices[0].message.content

        return response


class GPT4(BaseLLM):
    """
    Class for GPT-4 LLM by OpenAI.

    Args:
        api_key(:obj:`str`, optional): API Key for OpenAI client.

    Example:

        .. code-block:: python

            from llmbox.llms import GPT4
            from llmbox.chat import Chat, Message, Role

            llm = GPT4()
            chat = Chat()

            chat.add_message(message=Message(text='How big is the earth?', role=Role.User))
            response = llm.generate(chat=chat)
            print(response)

            chat.add_message(message=Message(text=response, role=Role.Assistant))
            chat.add_message(message=Message(text='What about the moon?', role=Role.User))
            next_response = llm.generate(chat=chat)
            print(next_response)
    """

    def __init__(self, api_key: str = None) -> None:
        # Initialize parent class
        super().__init__(creator=LLMCreator.OPENAI)

        # Verify authentication
        if api_key is None and os.environ.get('OPENAI_API_KEY') is None:
            raise ValueError('API key not found. '
                             'Set the environment variable OPENAI_API_KEY with your API key (recommended) or '
                             'pass the API key using the `api_key` argument while initializing the class.')

        # Initialize OpenAI client
        self._openai = openai
        if api_key is not None:
            self._openai.api_key = api_key
        else:
            self._openai.api_key = os.environ['OPENAI_API_KEY']

    def generate(
        self,
        chat: Chat,
        max_tokens: int = None,
        stop_sequences: list[str] = None,
        temperature: float = None,
        top_p: float = None
    ) -> str:
        """
        Generate response to a prompt.

        Args:
            chat(Chat): Chat containing the messages.
            max_tokens(:obj:`int`, optional): Maximum number of tokens to generate before stopping.
            stop_sequences(:obj:`list(str)`, optional): Sequences to stop generating completion text.
            temperature(:obj:`float`, optional): Amount of randomness injected into the response.
            top_p(:obj:`float`, optional): Cutoff probability for nucleus sampling of each subsequent token.

        Returns:
            str: Generated response from the LLM

        Example:

        .. code-block:: python

            from llmbox.llms import GPT35Turbo
            from llmbox.chat import Chat, Message, Role

            llm = GPT35Turbo()
            chat = Chat()

            chat.add_message(message=Message(text='How big is the earth?', role=Role.User))
            response = llm.generate(chat=chat)
            print(response)
        """

        # Create arguments for LLM generation
        generation_arguments = {
            'model': 'gpt-4',
            'messages': chat.generate_messages_openai()
        }
        generation_optionals = ['max_tokens', 'stop_sequences', 'temperature', 'top_p']
        for argument in generation_optionals:
            if eval(argument) is not None:
                generation_arguments[argument] = eval(argument)

        # Generate response
        response = openai.ChatCompletion.create(**generation_arguments).choices[0].message.content

        return response
