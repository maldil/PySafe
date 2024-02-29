import re
import statistics
import subprocess

from codewatchers.errors.all_error import AllErrors
from codewatchers.errors.radon_error import RadonError
from codewatchers.ichecker import IChecker


class NoComplexityDataException(Exception):
    pass


class NoMaintainabilityException(Exception):
    pass


class NoHalsteadMetricsException(Exception):
    pass


class Radon(IChecker):
    def run_analysis(self, code: str) -> AllErrors:
        temp_file_path = self.write_code_to_temp_file(code)
        errors = AllErrors()
        command = ['radon', 'cc', temp_file_path]
        result = subprocess.run(command, capture_output=True, text=True)
        try:
            cyclomatic_complexity = Radon.extract_cyclomatic_complexity(result.stdout)
            command = ['radon', 'mi', temp_file_path]
            result = subprocess.run(command, capture_output=True, text=True)
            try:
                maintainability_index = Radon.extract_maintainability_index(result.stdout)
                command = ['radon', 'hal', temp_file_path]
                result = subprocess.run(command, capture_output=True, text=True)
                try:
                    halstead_metric = Radon.extrac_halstead_metric(result.stdout)
                    r_error = RadonError(str(cyclomatic_complexity) + maintainability_index + halstead_metric,
                                         cyclomatic_complexity, maintainability_index, halstead_metric)
                    errors.add_item(r_error)
                    return errors
                except NoHalsteadMetricsException as e:
                    return errors
            except NoMaintainabilityException as e:
                return errors
        except NoComplexityDataException as e:
            return errors

    @staticmethod
    def extrac_halstead_metric(output: str):
        pattern = r'difficulty: ([\d.]+)'
        match = re.search(pattern, output)
        if match:
            return match.group(1)
        else:
            raise NoHalsteadMetricsException()

    @staticmethod
    def extract_maintainability_index(output: str):
        pattern = r'- (\w)\b'
        match = re.search(pattern, output)
        if match:
            return match.group(1)
        else:
            raise NoMaintainabilityException("No maintainability index found.")

    @staticmethod
    def extract_cyclomatic_complexity(output: str):
        pattern = r'F (\d+):\d+ \w+ - [A-F]'
        matches = re.findall(pattern, output)
        if len(matches) > 0:
            return statistics.mean([int(match) for match in matches])
        else:
            raise NoComplexityDataException("No cyclomatic complexity data found.")
