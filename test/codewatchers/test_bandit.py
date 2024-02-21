import unittest

from codewatchers.bandit import Bandit


class TestBanditAnalysis(unittest.TestCase):
    def setUp(self):
        self.bandit = Bandit()

    def test_analyze_function_with_bandit_password_issue(self):
        # Sample code that includes a security risk
        code = """
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
        results = self.bandit.run_analysis(code)

        # Check if the results contain an issue related to hardcoded passwords
        found_password_issue = any(
            "hardcoded password" in issue.get_issue().lower() for issue in results.get_all_errors()
        )

        self.assertTrue(found_password_issue, "No hardcoded password issue found.")

    # 1. Injection Flaws: SQL Injection
    def test_sql_injection_detection(self):
        code = """
import sqlite3
def get_user_details(user_id):
    conn = sqlite3.connect('example.db')
    query = f"SELECT * FROM users WHERE id = '{user_id}'"  # Potential SQL injection
    return conn.execute(query)
"""
        results = self.bandit.run_analysis(code)
        print(results)
        self.assertTrue(any("sql injection" in issue.get_issue().lower() for issue in results.get_all_errors()), "SQL Injection not detected.")

    # 2. Hardcoded Sensitive Data: Hardcoded Passwords
    def test_hardcoded_password_detection(self):
        code = """
def example_function():
    password = "password123"  # Example of a hardcoded password
"""
        results = self.bandit.run_analysis(code)
        self.assertTrue(any("hardcoded password" in issue.get_issue().lower() for issue in results.get_all_errors()),
                        "Hardcoded password not detected.")

    # 3. Insecure Use of Cryptography: Weak Cryptography
    def test_weak_cryptography_detection(self):
        code = """
import hashlib
def insecure_md5_hashing(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()  # Weak hashing algorithm
"""
        results = self.bandit.run_analysis(code)
        self.assertTrue(any("md5" in issue.get_issue().lower() for issue in results.get_all_errors()), "Weak cryptography (MD5) not detected.")

    # 8. General Code Issues: Use of exec
    def test_use_of_exec_detection(self):
        code = """
exec('print("Executing arbitrary code")')  # Potential security risk
"""
        results = self.bandit.run_analysis(code)
        self.assertTrue(any("use of exec" in issue.get_issue().lower() for issue in results.get_all_errors()),
                        "Use of exec not detected.")
