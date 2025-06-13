import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.call_function import call_function


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = " ".join(args)

    if verbose:
        print(f"Working on: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    generate_content(client, messages, verbose)


def get_schema_get_files_info():
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
    return schema_get_files_info


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


def get_schema_write_file():
    schema = types.FunctionDeclaration(
        name="write_file",
        description="Take file_path and content args and write content on file_path, the file_path is constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to write content to, relative to the working directory. It must be provided",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content that will be writen on file_path. It must be provided",
                ),
            },
        ),
    )
    return schema


def get_schema_run_python_file():
    schema = types.FunctionDeclaration(
        name="run_python_file",
        description="Run the python file specified by file_path, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to python file to run, relative to the working directory. It must be provided",
                ),
            },
        ),
    )
    return schema


def get_available_functions():
    schema_get_files_info = get_schema_get_files_info()
    schema_get_file_content = get_schema_get_file_content()
    schema_write_file = get_schema_write_file()
    schema_run_python_file = get_schema_run_python_file()
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )
    return available_functions


def generate_content(client, messages, verbose=False):
    available_functions = get_available_functions()
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if not response.function_calls:
        print("Response:")
        print(response.text)
    else:
        for function_call_part in response.function_calls:
            # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            try:
                function_call_result = call_function(function_call_part, verbose)
                function_response = function_call_result.parts[
                    0
                ].function_response.response
                if function_response and verbose:
                    print(f"-> {function_response}")
            except Exception as e:
                raise e


if __name__ == "__main__":
    main()
