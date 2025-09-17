import sys


def main():
    # Wait for user input
    while True:
        command = input("$ ")
        if command == "exit 0":
            sys.exit(0)
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
