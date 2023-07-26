import abc
from enum import Enum


class LLMAuthor(Enum):
    """Determines the author of an LLM."""

    ANTHROPIC = 1


class BaseLLM(abc.ABC):
    """Represents an LLM."""

    def __init__(self, author: LLMAuthor):
        self._author = author
