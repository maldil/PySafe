import re
from typing import List, Dict


def decode_error_output(output: str, regex_pattern) -> List[Dict[str, str]]:
    decoded_message = []
    for error in output.split('\n'):
        match = re.match(regex_pattern, error)
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

