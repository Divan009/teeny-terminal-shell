import sys


class Command:
    def run(self, args: str):
        raise NotImplementedError


class Echo(Command):
    def run(self, args: str):
        print(args)


class Exit(Command):
    def run(self, args: str):
        sys.exit(0)


class Type(Command):
    def __init__(self, registry):
        self.registry = registry

    def run(self, args):
        if args in self.registry:
            print(f"{args} is a shell builtin command")
        else:
            print(f"{args}: not found")


def main():
    # Wait for user input
    registry = {
        "echo": Echo(),
        "exit": Exit(),
    }
    # making this a key in register
    registry["type"] = Type(registry)

    while True:
        command = input("$ ").strip()
        if not command:
            continue
        cmd, *rest = command.split(" ", 1)
        args = rest[0] if rest else ""

        if cmd in registry:
            registry[cmd].run(args)
        else:
            print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
