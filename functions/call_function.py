from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python import run_python_file
from google.genai import types

functions_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python": run_python_file,
}


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args
    args["working_directory"] = "./calculator"

    if verbose:
        print(f"calling function: {function_name}({args})")

    print(f" - Calling function: {function_name}")

    if function_call_part.name not in functions_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    try:
        function_result = functions_map[function_name](**args)
        result = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name, response={"result": function_result}
                )
            ],
        )
    except Exception as e:
        result = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={
                        "error": f"Error while executing function: {function_name}:{e}"
                    },
                )
            ],
        )
    return result
