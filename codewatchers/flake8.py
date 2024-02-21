import os
import re
import subprocess
import tempfile
from typing import List, Dict

from codewatchers.errors.all_error import AllErrors
from codewatchers.errors.flake8_error import Flake8Error
from codewatchers.ichecker import IChecker


class Flake8(IChecker):
    def run_analysis(self, code: str) -> AllErrors:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "temp_code.py")
            with open(temp_file_path, 'w') as temp_code_file:
                temp_code_file.write(code)

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
    def decode_flake8_output(output: str) -> List[Dict[str, str]]:
        pattern = r'^(.*?):(\d+):(\d+): (\w+) (.*)$'
        decoded_message = []
        for error in output.split('\n'):
            match = re.match(pattern, error)
            if match:
                file_path = match.group(1)
                line_number = match.group(2)
                column_number = match.group(3)
                error_code = match.group(4)
                error_message = match.group(5)
                decoded_message.append(
                    {"File_Path": file_path, "Line_number": line_number, "Column_Number": column_number,
                     "Error_Code": error_code, "Error_Message": error_message})
        return decoded_message
