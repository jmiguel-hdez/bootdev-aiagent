import sys


def main():
    if len(sys.argv) < 2:
        print("Error: need to pass an argument")
    text = "\n".join(sys.argv[1:])
    print(text)


if __name__ == "__main__":
    main()
