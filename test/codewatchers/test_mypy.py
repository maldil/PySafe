import unittest

from codewatchers.mypy import MyPy


class TestMyPy(unittest.TestCase):
    def setUp(self) -> None:
        self.analyzer = MyPy()

    def test_mypy_test1(self):
        test_code = """
def add_numbers(a: int, b: int) -> int:
    return a + 'b'  # This should cause a type error
"""
        all_errors = self.analyzer.run_analysis(test_code)
        self.assertTrue(any("Unsupported operand types" in error.get_key() for error in all_errors.get_all_errors()))

    def test_mypy_test_unsupported_operands(self):
        test_code = """
def add_numbers(a: int, b: int) -> int:
    return a + 'b'  # This should cause a type error
"""
        all_errors = self.analyzer.run_analysis(test_code)
        self.assertTrue(any("Unsupported operand types" in error.get_key() for error in all_errors.get_all_errors()))

    def test_mypy_test_incompatible_return_type(self):
        test_code = """
def get_number() -> int:
    return 'not a number'  # This should cause a type error
"""
        all_errors = self.analyzer.run_analysis(test_code)
        self.assertTrue(
            any("Incompatible return value type" in error.get_key() for error in all_errors.get_all_errors()))

    def test_mypy_test_missing_return(self):
        test_code = """
def might_not_return(a: int) -> int:
    if a > 0:
        return a
    # Missing return statement otherwise
"""
        all_errors = self.analyzer.run_analysis(test_code)
        self.assertTrue(any("Missing return statement" in error.get_key() for error in all_errors.get_all_errors()))

    def test_mypy_test_argument_type_mismatch(self):
        test_code = """
def increment(number: int) -> int:
    return number + 1

result = increment('this is a string')  # This should cause a type error
"""
        all_errors = self.analyzer.run_analysis(test_code)
        self.assertTrue(any("has incompatible type" in error.get_key() for error in all_errors.get_all_errors()))

    def test_mypy_test_undefined_variable(self):
        test_code = """
def print_number():
    print(number)  # This should cause a type error

number = 5
"""
        all_errors = self.analyzer.run_analysis(test_code)
        self.assertTrue(
            any("missing a return type annotation " in error.get_key() for error in all_errors.get_all_errors()))
