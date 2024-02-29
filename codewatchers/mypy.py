from codewatchers.ichecker import IChecker
from codewatchers.errors.all_error import AllErrors
from codewatchers.errors.mypy_error import MyPyError
import subprocess
import tempfile
import os
from pathlib import Path
from codewatchers import util_functions
import re
class MyPy(IChecker):
    def run_analysis(self, code: str) -> AllErrors:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "temp_code.py")

            with open(temp_file_path, 'w') as temp_code_file:
                temp_code_file.write(code)

            current_script = Path(__file__).resolve()
            project_root = current_script.parent.parent
            config_path = project_root / 'configurations/mypy.ini'
            command = ['mypy', temp_file_path, '--config-file', config_path]
            result = subprocess.run(command, text=True, capture_output=True)
            pattern = r"(?P<file_path>.+?):(?P<line_number>\d+): error: (?P<error_message>.+?\[.+?\])"

            # Find all matches of the pattern in the mypy output
            matches = re.finditer(pattern, result.stdout)

            error = AllErrors()
            for match in matches:
                file_path = match.group('file_path')
                line_number = match.group('line_number')
                error_message = match.group('error_message')
                mypy_error = MyPyError(error_message,error_message,int(line_number))
                error.add_item(mypy_error)
        return error

    @staticmethod
    def decode_mypy_output(result: str):
        return util_functions.decode_error_output(result, r'^(.*?):(\d+):(\d+): (\w+) (.*)$')