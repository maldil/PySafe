import unittest

from codewatchers.flake8 import Flake8


class TestFlake8Analysis(unittest.TestCase):
    def setUp(self):
        self.analyzer = Flake8()

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
