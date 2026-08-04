import os.path

from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(absolute, file_path))
        if os.path.commonpath([absolute, abs_file_path]) != absolute:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        raise OSError(e)
