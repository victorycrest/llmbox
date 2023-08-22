from abc import ABC, abstractmethod
from enum import Enum


class LLMCreator(Enum):
    """List of LLM creators."""

    ANTHROPIC = 'anthropic'
    OPENAI = 'openai'


class BaseLLM(ABC):
    """
    Base class for LLMs.

    Args:
        creator(:obj:`LLMCreator`): Creator of the LLM
    """

    def __init__(self, creator: LLMCreator) -> None:
        self._creator = creator

    @abstractmethod
    def generate(self, **kwargs):
        pass

    @property
    def creator(self) -> str:
        """str: Creator of the LLM."""

        return self._creator.name
