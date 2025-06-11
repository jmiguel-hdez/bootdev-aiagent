import os

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    abs_workingdir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(abs_workingdir, file_path))
    if not target_path.startswith(abs_workingdir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_path, "r") as f:
            file_content_str = f.read(MAX_CHARS)
            file_content_extra = f.read()
            if file_content_extra:
                file_content_str += (
                    f'\n[...File "{file_path}" truncated at 10000 characters]\n'
                )
            return file_content_str

    except Exception as e:
        return f"Error: File could not by read with error: {e}"
