import subprocess

from codewatchers import util_functions
from codewatchers.all_test_runner import AllErrors
from codewatchers.errors.pylint_error import PyLintError
from codewatchers.ichecker import IChecker


class PyLint(IChecker):
    def run_analysis(self, code: str) -> AllErrors:
        temp_file_path = self.write_code_to_temp_file(code)
        result = subprocess.run(["pylint", temp_file_path], capture_output=True, text=True)
        decoded_results = util_functions.decode_error_output(result.stdout, '^(.*?):(\d+):(\d+): (\w+): (.*)$')
        all_errors = AllErrors()
        for decoded_result in decoded_results:
            flake_error = PyLintError(decoded_result["Error_Code"] + " " + decoded_result["Error_Message"],
                                      decoded_result["Error_Message"],
                                      int(decoded_result["Line_number"]))
            all_errors.add_item(flake_error)
        return all_errors
