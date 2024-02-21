import unittest

from codewatchers.pyright import PyRight


class TestPyRightAnalysis(unittest.TestCase):
    def setUp(self) -> None:
        self.pyright = PyRight()

    def test_not_defined_variables(self):
        code = """
        import sqlite3
        def get_user_details(user_id):
            query = f"SELECT * FROM users WHERE id = '{user_id}'"  # Potential SQL injection
            return conn.execute(query)
        """
        errors = self.pyright.run_analysis(code)
        self.assertTrue(any("is not defined" in error.get_issue().lower() for error in errors.get_all_errors()))

    def test_type_mismatch_error(self):
        code = """
        def add_numbers(a: int, b: int) -> int:
            return a + b
        result = add_numbers("5", "10")
        """
        errors = self.pyright.run_analysis(code)
        self.assertTrue(any(
            "cannot be assigned to parameter \"a\" of type \"int\"" in error.get_issue().lower() for error in
            errors.get_all_errors()))

    def test_unbound_variable(self):
        code = """
        if False:
            x = 10
        
        # Pyright will identify that 'x' might not be defined at this point.
        print(x)
        """
        errors = self.pyright.run_analysis(code)
        self.assertTrue(any(
            "\"x\" is not defined" in error.get_issue().lower() for error in
            errors.get_all_errors()))

    def test_missing_return_statement(self):
        code = """
        def get_number() -> int:
            a = 5
        print(get_number())
        """
        errors = self.pyright.run_analysis(code)
        self.assertTrue(any(
            "type \"int\" must return value on all code paths" in error.get_issue().lower() for error in
            errors.get_all_errors()))

    def test_unused_variable(self):
        code = """
        def calculate_sum(a: int, b: int) -> int:
            total = a + b
            # Pyright can be configured to identify unused variables.
            # In this case, 'result' is defined but not used.
            result = total * 2
            return total
        """
        errors = self.pyright.run_analysis(code)
        self.assertTrue(any(
            "reportunusedvariable" in error.get_issue().lower() for error in
            errors.get_all_errors()))
