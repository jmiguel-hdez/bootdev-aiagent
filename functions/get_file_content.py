import os
from config import MAX_CHARS
from google.genai import types


def get_schema_get_file_content():
    schema = types.FunctionDeclaration(
        name="get_file_content",
        description="get text content of specified file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to get the content from, relative to the working directory. It must be provided",
                ),
            },
        ),
    )
    return schema


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
                    f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]\n'
                )
            return file_content_str

    except Exception as e:
        return f'Error: could not read file:"{file_path}" exception: {e}'
