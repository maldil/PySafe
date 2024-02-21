from typing import List
from codewatchers.errors.all_error import AllErrors
from codewatchers.ichecker import IChecker


class UnsupportedChecker(Exception):
    def __init__(self, message):
        super().__init__(message)


class CodeChecker:
    def __init__(self):
        self.tests: List[IChecker] = []

    def register_test(self, test: IChecker):
        if isinstance(test, IChecker):
            self.tests.append(test)
        else:
            raise UnsupportedChecker(type(test).__name__ + "is not a supported test type")

    def run_all_tests(self, code: str)-> AllErrors:
        all_errors = AllErrors()
        for test in self.tests:
            all_errors.extend(test.run_analysis(code))
        return all_errors

