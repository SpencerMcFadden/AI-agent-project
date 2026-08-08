import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text content to a specified file within the working directory (overwriting if the file exists)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to target file, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write into the target file"
                }
            },
            "required": ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute, file_path))
        if os.path.commonpath([absolute, target_dir]) != absolute:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        with open(target_dir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        raise OSError(e)
