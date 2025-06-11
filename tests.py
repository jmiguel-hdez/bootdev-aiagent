from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

test_get_files_info = False
tests_get_files_info = []
if test_get_files_info:
    tests_get_files_info = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../"),
    ]

test_content = True
test_ipsum = False
tests_get_file_content = []
if test_content:
    tests_get_file_content = [
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
    ]


def test_ipsum_content(
    test_ipsum=True, working_directory="calculator", filename="lorem.txt"
):
    if test_ipsum:
        print("testing ipsum file content")
        result = get_file_content(working_directory, filename)
        print(result)
        assert "truncated at 10000 characters" in result


def test():
    for workingdir, directory in tests_get_files_info:
        print(f"Result for workingdir:{workingdir} directory:{directory}")
        result = get_files_info(workingdir, directory)
        print(result)
    test_ipsum_content(test_ipsum)

    for workindir, filename in tests_get_file_content:
        print(f"Result for workindir:{workindir} filename: {filename}")
        result = get_file_content(workindir, filename)
        print(result)


if __name__ == "__main__":
    test()
