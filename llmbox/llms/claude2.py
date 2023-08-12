from anthropic import Anthropic

from .base import BaseLLM, LLMCreator


class Claude2(BaseLLM):
    """
    Class for Claude 2 LLM by Anthropic.

    Args:
        auth_token(str | None): Authentication token for accessing Anthropic LLMs
        api_key(str | None): API Key for accessing Anthropic LLMs
    """

    def __init__(self, auth_token: str | None = None, api_key: str | None = None):
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

            from llmbox.llms import Claude2
            llm = Claude2()
            response = llm.generate(prompt='\n\nHuman: How far is the moon from the earth? \n\nAssistant:')
            print(response)
        """

        return self._anthropic.completions.create(
            prompt=prompt,
            model='claude-2',
            max_tokens_to_sample=max_tokens_to_sample
        ).completion
