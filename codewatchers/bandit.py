import os
import tempfile

from bandit.core.config import BanditConfig
from bandit.core.manager import BanditManager

from codewatchers.errors.all_error import AllErrors
from codewatchers.errors.bandit_error import BanditError
from codewatchers.ichecker import IChecker


class Bandit(IChecker):
    def run_analysis(self, function_code: str) -> AllErrors:

        """
        Analyzes the given function code with Bandit for security issues and returns a list of found issues.

        Args:
            function_code (str): The source code of the function to analyze.

        Returns:
            list: A list of dictionaries, each representing an issue found by Bandit.
        """
        # Use tempfile in a context manager to ensure it's properly closed
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as tmp:
            tmp_file_name = tmp.name
            tmp.write(function_code.encode('utf-8'))
        errors = AllErrors()
        try:
            b_config = BanditConfig()

            b_manager = BanditManager(
                config=b_config,
                agg_type='file',
                debug=False,
                verbose=False,
                quiet=True,
                profile=None,
                ignore_nosec=False
            )

            # Assign the target files directly
            b_manager.targets = [tmp_file_name]

            # Discover files and run tests
            b_manager.discover_files([tmp_file_name])
            b_manager.run_tests()

            for error in b_manager.get_issue_list():
                bandit_error = BanditError(error.text, error.text, error.severity, error.confidence, error.lineno)
                errors.add_item(bandit_error)

        except Exception as e:
            print(f"An error occurred during Bandit analysis: {e}")
        finally:
            # Ensure the temporary file is removed after analysis
            os.remove(tmp_file_name)
        return errors
