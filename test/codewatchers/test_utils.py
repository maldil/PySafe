import unittest
from codewatchers.util_functions import decode_error_output as decode_flake8_output


class TestUtils(unittest.TestCase):
    def test_syntax_error(self):
        output = "/path/to/file.py:1:1: E999 SyntaxError: invalid syntax"
        expected = [{
            "File_Path": "/path/to/file.py",
            "Line_number": "1",
            "Column_Number": "1",
            "Error_Code": "E999",
            "Error_Message": "SyntaxError: invalid syntax"
        }]
        result = decode_flake8_output(output, r'^(.*?):(\d+):(\d+): (\w+) (.*)$')
        self.assertEqual(result, expected)

    def test_indentation_error(self):
        output = "/path/to/file.py:2:5: E117 over-indented"
        expected = [{
            "File_Path": "/path/to/file.py",
            "Line_number": "2",
            "Column_Number": "5",
            "Error_Code": "E117",
            "Error_Message": "over-indented"
        }]
        result = decode_flake8_output(output,r'^(.*?):(\d+):(\d+): (\w+) (.*)$')
        self.assertEqual(result, expected)

    def test_unused_import(self):
        output = "/path/to/file.py:3:1: F401 'os' imported but unused"
        expected = [{
            "File_Path": "/path/to/file.py",
            "Line_number": "3",
            "Column_Number": "1",
            "Error_Code": "F401",
            "Error_Message": "'os' imported but unused"
        }]
        result = decode_flake8_output(output,r'^(.*?):(\d+):(\d+): (\w+) (.*)$')
        self.assertEqual(result, expected)

    def test_line_too_long(self):
        output = "/path/to/file.py:4:80: E501 line too long (90 > 79 characters)"
        expected = [{
            "File_Path": "/path/to/file.py",
            "Line_number": "4",
            "Column_Number": "80",
            "Error_Code": "E501",
            "Error_Message": "line too long (90 > 79 characters)"
        }]
        result = decode_flake8_output(output,r'^(.*?):(\d+):(\d+): (\w+) (.*)$')
        self.assertEqual(result, expected)

    def test_undefined_name(self):
        output = "/path/to/file.py:5:1: F821 undefined name 'undefined_var'"
        expected = [{
            "File_Path": "/path/to/file.py",
            "Line_number": "5",
            "Column_Number": "1",
            "Error_Code": "F821",
            "Error_Message": "undefined name 'undefined_var'"
        }]
        result = decode_flake8_output(output,r'^(.*?):(\d+):(\d+): (\w+) (.*)$')
        self.assertEqual(result, expected)

    def test_multiple_errors(self):
        output = """
/path/to/file.py:1:1: E999 SyntaxError: invalid syntax
/path/to/file.py:2:5: E117 over-indented
/path/to/file.py:3:1: F401 'os' imported but unused
    """
        expected = [
            {"File_Path": "/path/to/file.py", "Line_number": "1", "Column_Number": "1", "Error_Code": "E999",
             "Error_Message": "SyntaxError: invalid syntax"},
            {"File_Path": "/path/to/file.py", "Line_number": "2", "Column_Number": "5", "Error_Code": "E117",
             "Error_Message": "over-indented"},
            {"File_Path": "/path/to/file.py", "Line_number": "3", "Column_Number": "1", "Error_Code": "F401",
             "Error_Message": "'os' imported but unused"}
        ]
        result = decode_flake8_output(output.strip(),r'^(.*?):(\d+):(\d+): (\w+) (.*)$')
        self.assertEqual(result, expected)
