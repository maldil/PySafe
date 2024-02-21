import unittest

from codewatchers.flake8 import Flake8


class TestFlake8Analysis(unittest.TestCase):
    def setUp(self):
        self.analyzer = Flake8()

    def test_analyze_function_(self):
        code = """import sqlite3
jjj
kk

def get_user_details(user_id):
    query = f"SELECT * FROM users WHERE id = '{user_id}'"  # Potential SQL injection
    return conn.execute(query)"""
        flake = Flake8()
        all_errors = flake.run_analysis(code)

    def test_syntax_error(self):
        output = "/path/to/file.py:1:1: E999 SyntaxError: invalid syntax"
        expected = [{
            "File_Path": "/path/to/file.py",
            "Line_number": "1",
            "Column_Number": "1",
            "Error_Code": "E999",
            "Error_Message": "SyntaxError: invalid syntax"
        }]
        result = Flake8.decode_flake8_output(output)
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
        result = Flake8.decode_flake8_output(output)
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
        result = Flake8.decode_flake8_output(output)
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
        result = Flake8.decode_flake8_output(output)
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
        result = Flake8.decode_flake8_output(output)
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
        result = Flake8.decode_flake8_output(output.strip())
        self.assertEqual(result, expected)

    def test_syntax_error(self):
        # E999 SyntaxError: invalid syntax
        code = "def invalid_syntax("
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("E999" in error.get_key() for error in all_errors.get_all_errors()))

    def test_indentation_error(self):
        # E117 over-indented
        code = """
def foo():
        print("over-indented")
"""
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("E117" in error.get_key() for error in all_errors.get_all_errors()))

    def test_unused_import(self):
        # F401 'module' imported but unused
        code = "import os"
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("F401" in error.get_key() for error in all_errors.get_all_errors()))

    def test_line_too_long(self):
        # E501 line too long
        code = '"' * 82
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("E999" in error.get_key() for error in all_errors.get_all_errors()))

    def test_undefined_name(self):
        # F821 undefined name
        code = "print(undefined_var)"
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("F821" in error.get_key() for error in all_errors.get_all_errors()))

    def test_missing_whitespace_around_operator(self):
        # E225 missing whitespace around operator
        code = "a=1+1"
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("E225" in error.get_key() for error in all_errors.get_all_errors()))

    def test_module_level_import_not_at_top_of_file(self):
        # E402 module level import not at top of file
        code = """
def dummy_function():
    pass
import os
"""
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("E402" in error.get_key() for error in all_errors.get_all_errors()))

    def test_too_many_blank_lines(self):
        # E303 too many blank lines
        code = """





def dummy_function():
    pass
"""
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("E303" in error.get_key() for error in all_errors.get_all_errors()))

    def test_trailing_whitespace(self):
        # W291 trailing whitespace
        code = "def foo(): \n    pass"
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("W291" in error.get_key() for error in all_errors.get_all_errors()))
