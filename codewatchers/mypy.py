import re
import subprocess
import tempfile
from pathlib import Path

from codewatchers import util_functions
from codewatchers.errors.all_error import AllErrors
from codewatchers.errors.mypy_error import MyPyError
from codewatchers.ichecker import IChecker


class MyPy(IChecker):
    @staticmethod
    def construct_mypy_command(temp_file_path: str) -> list:
        config_path = Path(__file__).resolve().parent.parent / 'configurations' / 'mypy.ini'
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        return ['mypy', temp_file_path, '--config-file', str(config_path)]

    @staticmethod
    def parse_mypy_output(output: str) -> AllErrors:
        all_errors = AllErrors()
        pattern = r"(?P<file_path>.+?):(?P<line_number>\d+): error: (?P<error_message>.+?\[.+?\])"
        for match in re.finditer(pattern, output):
            error_message = match.group('error_message')
            mypy_error = MyPyError(error_message, error_message, int(match.group('line_number')))
            all_errors.add_item(mypy_error)
        return all_errors

    def run_analysis(self, code: str) -> AllErrors:
        temp_file_path = self.write_code_to_temp_file(code)
        command = self.construct_mypy_command(temp_file_path)

        try:
            result = subprocess.run(command, text=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            # Handle subprocess errors, e.g., command execution failure
            raise RuntimeError(f"Failed to run analysis: {e}")

        all_errors = self.parse_mypy_output(result.stdout)
        return all_errors

    @staticmethod
    def decode_mypy_output(result: str):
        return util_functions.decode_error_output(result, r'^(.*?):(\d+):(\d+): (\w+) (.*)$')
