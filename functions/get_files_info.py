import os
from pathlib import Path


def get_files_info(working_directory, directory=None):
    working_directory_abs = os.path.abspath(working_directory)
    # print(f"working_directory_abs({working_directory_abs})")
    target_directory = working_directory_abs

    if directory:
        target_directory = os.path.abspath(
            os.path.join(working_directory_abs, directory)
        )

    if not str(target_directory).startswith(str(working_directory_abs)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'

    try:
        file_info = []
        for path in os.listdir(target_directory):
            filepath = os.path.join(target_directory, path)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            file_info.append(f"- {path}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(file_info)
    except Exception as e:
        return f"Error listing files: {e}"
