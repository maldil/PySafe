import subprocess
import tempfile
import json
import os
from pathlib import Path
from codewatchers.errors.all_error import AllErrors
from codewatchers.errors.pyright_error import PyRightError
from codewatchers.ichecker import IChecker


# Pyright: Developed by Microsoft, Pyright is a fast type checker that can run in a strict mode
# or a more permissive mode. It is designed to catch type errors and other common mistakes in
# Python code, especially in codebases that use type annotations.


class PyRight(IChecker):
    def run_analysis(self, function_code: str):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "temp_code.py")
            config_file_path = os.path.join(temp_dir, "pyrightconfig.json")

            with open(temp_file_path, 'w') as temp_file:
                temp_file.write(function_code)

            current_script = Path(__file__).resolve()
            project_root = current_script.parent.parent
            config_path = project_root / 'configurations/pyrightconfig.json'

            with open(config_path) as f:
                pyright_config = json.load(f)

            with open(config_file_path, 'w') as config_file:
                json.dump(pyright_config, config_file)

            result = subprocess.run(['pyright', '--project', temp_dir, temp_file_path], capture_output=True, text=True)

            errors = [(message.split(":")[1],message.split(":")[3].strip()) for message in result.stdout.split('\n') if "error:" in message]
            all_errors = AllErrors()
            for error in errors:
                pyright_error = PyRightError(error[1], error[1], int(error[0]))
                all_errors.add_item(pyright_error)

            return all_errors

