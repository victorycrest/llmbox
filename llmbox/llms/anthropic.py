from enum import Enum

from anthropic import Anthropic

from .base import BaseLLM, LLMCreator


class AnthropicModels(Enum):
    """
    List of Anthropic models.
    """

    CLAUDEINSTANT1 = 'claude-instant-1'
    CLAUDE2 = 'claude-2'


class AnthropicLLM(BaseLLM):
    """
    Class for LLMs by Anthropic.

    Args:
        auth_token(str | None): Authentication token for accessing Anthropic LLMs
        api_key(str | None): API Key for accessing Anthropic LLMs
    """

    _model = AnthropicModels.CLAUDE2

    def __init__(self, auth_token: str = None, api_key: str = None):
        super().__init__(creator=LLMCreator.ANTHROPIC)
        self._anthropic = Anthropic(auth_token=auth_token, api_key=api_key)

    def generate(self, prompt: str, max_tokens_to_sample: int = 1000) -> str:
        """
        Generate response to a prompt.

        Args:
            prompt(str): Prompt
            max_tokens_to_sample(int): Maximum number of tokens to generate

        Returns:
            str: Generated response from the LLM

        Example:

        .. code-block:: python

            from llmbox.llms import ClaudeInstant1, Claude2

            llm1 = ClaudeInstant1()
            response1 = llm1.generate(prompt='\\n\\nHuman: How big is the earth? \\n\\nAssistant:')
            print(response1)

            llm2 = Claude2()
            response2 = llm2.generate(prompt='\\n\\nHuman: How big is the earth? \\n\\nAssistant:')
            print(response2)
        """

        return self._anthropic.completions.create(
            prompt=prompt,
            model=str(self._model.value),
            max_tokens_to_sample=max_tokens_to_sample
        ).completion


class ClaudeInstant1(AnthropicLLM):
    """
    Class for Claude-Instant-1 LLM by Anthropic.

    Args:
        auth_token(str | None): Authentication token for accessing Claude-Instant-1 LLM
        api_key(str | None): API Key for accessing Claude-Instant-1 LLM

    Example:

    .. code-block:: python

        from llmbox.llms import ClaudeInstant1

        llm = ClaudeInstant1()
        response = llm.generate(prompt='\\n\\nHuman: How big is the earth? \\n\\nAssistant:')
        print(response)
    """

    _model = AnthropicModels.CLAUDEINSTANT1


class Claude2(AnthropicLLM):
    """
    Class for Claude-2 LLM by Anthropic.

    Args:
        auth_token(str | None): Authentication token for accessing Claude-2 LLM
        api_key(str | None): API Key for accessing Claude-2 LLM

    Example:

    .. code-block:: python

        from llmbox.llms import ClaudeInstant1

        llm = Claude2()
        response = llm.generate(prompt='\\n\\nHuman: How big is the earth? \\n\\nAssistant:')
        print(response)
    """

    _model = AnthropicModels.CLAUDE2
