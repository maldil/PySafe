import unittest
from codewatchers.radon import Radon


class TestRadon(unittest.TestCase):
    def setUp(self) -> None:
        self.model = Radon()

    def test_radon_error1(self):
        code_to_analyze = """
def simple_function():
    return "Hello, World!"

def complex_function(x):
    if x < 10:
        return "Less than 10"
    elif x < 20:
        return "Between 10 and 20"
    else:
        return "20 or more"
"""
        a_error = self.model.run_analysis(code=code_to_analyze)
        self.assertEqual(a_error.get_all_errors()[0].get_cyclomatic_complexity(),3.5)

    def test_simple_function_complexity(self):
        code_to_analyze = """
def simple_function():
    return "Hello, World!"
"""
        analysis_result = self.model.run_analysis(code=code_to_analyze)
        # Assuming the first error corresponds to the `simple_function`
        self.assertEqual(analysis_result.get_all_errors()[0].get_cyclomatic_complexity(), 2)

    def test_complex_function_complexity(self):
        code_to_analyze = """
def complex_function(x):
    if x < 10:
        return "Less than 10"
    elif x < 20:
        return "Between 10 and 20"
    else:
        return "20 or more"
"""
        analysis_result = self.model.run_analysis(code=code_to_analyze)
        # Assuming the first error corresponds to the `complex_function`
        self.assertEqual(analysis_result.get_all_errors()[0].get_cyclomatic_complexity(), 2)

    def test_combined_complexity(self):
        code_to_analyze = """
def simple_function():
    return "Hello, World!"

def complex_function(x):
    if x < 10:
        return "Less than 10"
    elif x < 20:
        return "Between 10 and 20"
    else:
        return "20 or more"
"""
        analysis_result = self.model.run_analysis(code=code_to_analyze)
        # Assuming we want the average complexity of all analyzed functions
        complexities = [error.get_cyclomatic_complexity() for error in analysis_result.get_all_errors()]
        average_complexity = sum(complexities) / len(complexities)
        self.assertAlmostEqual(average_complexity, 3.5)  # Assuming there are 2 functions, one with CC=1, another with CC=3
