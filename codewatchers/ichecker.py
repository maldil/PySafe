from abc import ABC, abstractmethod
from codewatchers.errors.all_error import AllErrors
import tempfile

class IChecker(ABC):
    @abstractmethod
    def run_analysis(self, code: str) -> AllErrors:
        pass

    @staticmethod
    def write_code_to_temp_file(code: str) -> str:
        with tempfile.NamedTemporaryFile(suffix=".py", mode='w', delete=False) as temp_code_file:
            temp_code_file.write(code)
            return temp_code_file.name
