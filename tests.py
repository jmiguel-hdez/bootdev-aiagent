from functions.get_files_info import get_files_info

tests = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../"),
]


def test():
    for workingdir, directory in tests:
        print(f"Result for workingdir:{workingdir} directory:{directory}")
        result = get_files_info(workingdir, directory)
        print(result)


if __name__ == "__main__":
    test()
