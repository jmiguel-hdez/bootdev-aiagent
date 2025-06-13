import os


def write_file(working_directory, file_path, content):
    abs_workingdir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(abs_workingdir, file_path))
    target_directory = os.path.dirname(target_path)

    if not target_path.startswith(abs_workingdir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_directory):
        try:
            os.makedirs(target_directory, exist_ok=True)
        except Exception as e:
            return f"Error: creating directory {target_directory}: {e}"

    if os.path.exists(target_path) and os.path.isdir(target_path):
        return f'Error "{file_path}" is a directory, not a file'

    try:
        with open(target_path, "w", encoding="utf-8") as f:
            wbytes = f.write(content)
            if wbytes == len(content):
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            else:
                return f'Error: Only {wbytes} from {len(content)} written for "{file_path}"'
    except Exception as e:
        return f'Error: Cannot write to "{file_path} due to error: {e}'
