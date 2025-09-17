import sys


def main():
    # Wait for user input
    while True:
        command = input("$ ")
        split_cmd = command.strip().split(" ", 1)
        if split_cmd[0] == "echo":
            print(split_cmd[-1])
        if split_cmd[0] == "exit":
            sys.exit(0)
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
