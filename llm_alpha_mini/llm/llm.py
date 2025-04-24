from abc import ABC, abstractmethod

class LLM(ABC):

    @abstractmethod
    def query(self, prompt: str) -> str:
        ...