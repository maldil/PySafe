import unittest
from codewatchers.bandit import Bandit
from codewatchers.pyright import PyRight
from codewatchers.all_test_runner import CodeChecker
from codewatchers.pylint import PyLint


class TestAllTestRunner(unittest.TestCase):
    def test_bandit_pychecker(self):
        bandit = Bandit()
        pyright = PyRight()
        code_checker = CodeChecker()
        code_checker.register_test(bandit)
        code_checker.register_test(pyright)
        code1 = """
def send_email():
    sender_email = "user@example.com"
    receiver_email = "receiver@example.com"
    password = "supersecretpassword"  
    message = "This is a test email message."

    import smtplib
    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        """

        test_results_code1 = code_checker.run_all_tests(code1)
        code2 = """
def send_email():
    receiver_email = "receiver@example.com"
    password = "supersecretpassword"  
    message = "This is a test email message."

    import smtplib
    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
"""
        test_results_code2 = code_checker.run_all_tests(code2)
        new_error_after_change = test_results_code1.get_additional_error(test_results_code2)
        self.assertTrue(any("reportUndefinedVariable" in error.get_key() for error in new_error_after_change))

    def test_bandit_pylint_pychecker(self):
        bandit = Bandit()
        pyright = PyRight()
        pylint = PyLint()
        code_checker = CodeChecker()
        code_checker.register_test(bandit)
        code_checker.register_test(pyright)
        code_checker.register_test(pylint)
        code1 = """
def send_email():
    sender_email = "user@example.com"
    receiver_email = "receiver@example.com"
    password = "supersecretpassword"  
    message = "This is a test email message."

    import smtplib
    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        """

        test_results_code1 = code_checker.run_all_tests(code1)
        code2 = """
def send_email():
    receiver_email = "receiver@example.com"
    password = "supersecretpassword"  
    message = "This is a test email message."
    a = "This is a very long line that should trigger the line too long linting error because it exceeds the maximum allowed length."
    import smtplib
    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
"""
        test_results_code2 = code_checker.run_all_tests(code2)
        new_error_after_change = test_results_code1.get_additional_error(test_results_code2)
        self.assertTrue(any("reportUndefinedVariable" in error.get_key() for error in new_error_after_change))
        self.assertTrue(any("C0301 Line too long" in error.get_key() for error in new_error_after_change))