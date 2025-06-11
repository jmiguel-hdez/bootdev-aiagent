import os
from pathlib import Path


def get_files_info(working_directory, directory=None):
    # print(f"get_files_info({working_directory},{directory})")
    working_directory_abs = os.path.abspath(working_directory)
    # print(f"working_directory_abs({working_directory_abs})")
    list_directory = working_directory_abs

    if directory:
        directory_abs = os.path.abspath(os.path.join(working_directory_abs, directory))
        # print(f"directory_abs({directory_abs})")
        if not str(directory_abs).startswith(str(working_directory_abs)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(directory_abs):
            return f'Error: "{directory}" is not a directory'
        list_directory = directory_abs

    file_info = []
    for path in os.listdir(list_directory):
        is_dir = os.path.isdir(os.path.join(list_directory, path))
        file_size = os.path.getsize(os.path.join(list_directory, path))
        file_info.append(f"- {path}: file_size={file_size} bytes, is_dir={is_dir}")

    return "\n".join(file_info)
