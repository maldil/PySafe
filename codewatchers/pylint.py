import os
import subprocess
import tempfile

from codewatchers import util_functions
from codewatchers.all_test_runner import AllErrors
from codewatchers.errors.pylint_error import PyLintError
from codewatchers.ichecker import IChecker


class PyLint(IChecker):
    def run_analysis(self, code: str) -> AllErrors:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "temp_code.py")
            with open(temp_file_path, 'w') as temp_code_file:
                temp_code_file.write(code)
            result = subprocess.run(["pylint", temp_file_path], capture_output=True, text=True)
            decoded_results = util_functions.decode_error_output(result.stdout, '^(.*?):(\d+):(\d+): (\w+): (.*)$')
            all_errors = AllErrors()
            for decoded_result in decoded_results:
                flake_error = PyLintError(decoded_result["Error_Code"] + " " + decoded_result["Error_Message"],
                                          decoded_result["Error_Message"],
                                          int(decoded_result["Line_number"]))
                all_errors.add_item(flake_error)
            return all_errors
