from abc import ABC, abstractmethod

class LLM(ABC):
    """
    Base class for all LLM classes, all LLM classes should inherit from LLM.
    """
    @abstractmethod
    def query(self, prompt: str) -> str:
        ...