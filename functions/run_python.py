import os
import subprocess
import shlex
import sys


def run_python_file(working_directory, file_path, args=None):
    # if the `file_path` is outside the working directory, return a string with an error
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # if the `file_path` doesn't exist, return an error string
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'

    # if the file doesn't end with ".py", return an error string:
    _, ext = os.path.splitext(target_path)
    if ext != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    # Use `subprocess.run` function to execute the Python file.
    # Set a timeout of 30 seconds to prevent infinite execution
    # Capture both stdout and stderr
    # Set the working directory properly
    pyexe = sys.executable
    cmd = shlex.split(f"{pyexe} {target_path}")
    if args:
        cmd.extend(args)
    result = ""
    try:
        cmdout = subprocess.run(
            cmd,
            timeout=30,
            check=True,
            text=True,
            capture_output=True,
            encoding="utf-8",
            cwd=abs_working_dir,
        )
        if len(cmdout.stdout) == 0 and len(cmdout.stderr) == 0:
            return "No output produced"
        result += f"STDOUT:\n{cmdout.stdout}\nSTDERR:\n{cmdout.stderr}\n"
    except subprocess.CalledProcessError as e:
        result += f"Process existed with code {e.returncode}\n"
    except Exception as e:
        result += f"Error: executing Python file: {e}\n"

    # Format the output to include:
    # The stdout prefixed with "STDOUT:"
    # The stderr(prefixed with "STDERR:")
    # if the process exists with a non-zero code, include "Process existed with code X"
    # if no output is produced, return "No output produced"
    # if any exceptions occure during execution, catch them and return an error string.
    # f'Error: executing Python file: {e}'
    return result
