import os.path
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes target pythole file with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to target file, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of optional arguments to pass to the target file for execution"
                }
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not abs_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", abs_file_path]
        if args:
            command.extend(args)
        subprocess_result = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
        return_str = ''
        if subprocess_result.returncode != 0:
            return_str += f'Process exited with code {subprocess_result.returncode}\n'
        if not subprocess_result.stdout and not subprocess_result.stderr:
            return_str += 'No output produced\n'
        if subprocess_result.stdout:
            return_str += f'STDOUT:\n{subprocess_result.stdout}'
        if subprocess_result.stderr:
            return_str += f'STDERR:\n{subprocess_result.stderr}'
        return return_str
    except Exception as e:
        raise OSError(e)
