import abc
from enum import Enum


class LLMCreator(Enum):
    """
    List of LLM creators.
    """

    ANTHROPIC = 1


class BaseLLM(abc.ABC):
    """
    Class for LLMs.

    Args:
        creator(LLMCreator): Creator of LLM
    """

    def __init__(self, creator: LLMCreator):
        self._creator = creator
