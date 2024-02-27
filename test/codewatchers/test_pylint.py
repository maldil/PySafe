import unittest

from codewatchers.pylint import PyLint


class TestPyLint(unittest.TestCase):
    def setUp(self):
        self.analyzer = PyLint()

    def test_linting_error_1(self):
        code = """def calculate_sum(a, b):
    result = a + b
    unused_variable = "I am not used anywhere"
    return result"""
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("missing-final-newline" in error.get_key() for error in all_errors.get_all_errors()))
        self.assertTrue(any("missing-module-docstring" in error.get_key() for error in all_errors.get_all_errors()))

    def test_linting_error_variable_naming(self):
        code = """
def calculate_difference(a, b):
    ResultValue = a - b
    return ResultValue
"""
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("invalid-name" in error.get_key() for error in all_errors.get_all_errors()))

    def test_linting_error_missing_type_hint(self):
        code = """
def add_numbers(a, b):
    return a + b
"""
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("missing-function-docstring" in error.get_key() for error in all_errors.get_all_errors()))

    def test_linting_error_too_many_arguments(self):
        code = """
def too_many_args(a, b, c, d, e, f, g):
    pass
"""
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("too-many-arguments" in error.get_key() for error in all_errors.get_all_errors()))

    def test_linting_error_line_too_long(self):
        code = 'a = "This is a very long line that should trigger the line too long linting error because it exceeds the maximum allowed length."'
        all_errors = self.analyzer.run_analysis(code)
        self.assertTrue(any("line-too-long" in error.get_key() for error in all_errors.get_all_errors()))

    def test_linting_error_import_not_at_top(self):
        code = """
def some_function():
    pass
import os
"""
        all_errors = self.analyzer.run_analysis(code)
        print(all_errors)
        self.assertTrue(any("wrong-import-position" in error.get_key() for error in all_errors.get_all_errors()))
