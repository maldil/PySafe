import subprocess

from codewatchers import util_functions
from codewatchers.errors.all_error import AllErrors
from codewatchers.errors.flake8_error import Flake8Error
from codewatchers.ichecker import IChecker


class Flake8(IChecker):
    def run_analysis(self, code: str) -> AllErrors:
        temp_file_path = self.write_code_to_temp_file(code)
        result = subprocess.run(['flake8', temp_file_path, '--select=E,W,F,C,N'], capture_output=True, text=True)
        decoded_results = Flake8.decode_flake8_output(result.stdout)
        all_errors = AllErrors()
        for decoded_result in decoded_results:
            flake_error = Flake8Error(decoded_result["Error_Code"] + " " + decoded_result["Error_Message"],
                                      decoded_result["Error_Message"],
                                      int(decoded_result["Line_number"]))
            all_errors.add_item(flake_error)
        return all_errors

    @staticmethod
    def decode_flake8_output(result: str):
        return util_functions.decode_error_output(result, r'^(.*?):(\d+):(\d+): (\w+) (.*)$')
