# providers/base_provider.py
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def generate_image(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def analyze_text(self, text: str, task: str, **kwargs) -> str:
        """Task could be 'grammar', 'plagiarism', 'ai-detect' etc."""
        pass
