from anthropic import Anthropic

from .base import BaseLLM, LLMAuthor


class Claude2(BaseLLM):
    def __init__(self, auth_token: str | None = None, api_key: str | None = None):
        super().__init__(author=LLMAuthor.ANTHROPIC)
        self._anthropic = Anthropic(auth_token=auth_token, api_key=api_key)

    def generate(self, prompt: str, max_tokens_to_sample: int = 1000):
        return self._anthropic.completions.create(
            max_tokens_to_sample=max_tokens_to_sample,
            model='claude-2',
            prompt=prompt
        ).completion.strip()
