import os.path

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute, directory))
        if os.path.commonpath([absolute, target_dir]) == absolute:
            if os.path.isdir(target_dir):
                contents = ''
                for item in os.listdir(target_dir):
                    path = os.path.join(target_dir, item)
                    contents += f'- {item}: file_size={os.path.getsize(path)}, is_dir={os.path.isdir(path)}\n'
                return contents
            else:
                return OSError(f'Error: "{directory}" is not a directory')
        else:
            return OSError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    except Exception as e:
        raise OSError(e)
    
