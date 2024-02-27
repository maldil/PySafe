from abc import ABC, abstractmethod
from codewatchers.errors.all_error import AllErrors


class IChecker(ABC):
    @abstractmethod
    def run_analysis(self, code: str) -> AllErrors:
        pass
