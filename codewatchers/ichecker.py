from abc import ABC, abstractmethod
from codewatchers.errors.ierror import IError


class IChecker(ABC):
    @abstractmethod
    def run_analysis(self, code: str) -> IError:
        pass
