from __future__ import annotations

from pathlib import Path
import os
import sys

from app.utils import _cmd_locator


class Command:
    def run(self, args: str):
        raise NotImplementedError

    def name(self) -> str:
        raise NotImplementedError


class Echo(Command):
    def run(self, args: str):
        print(args)

    def name(self) -> str:
        return "echo"


class Pwd(Command):
    def run(self, args: str):
        print(os.getcwd())

    def name(self) -> str:
        return "pwd"


class Cd(Command):
    def run(self, args: str):

        if not args or args == "~":
            target = Path.home()
        else:
            target = Path(args)

        try:
            os.chdir(target)
        except FileNotFoundError as e:
            print(f"cd: {target}: No such file or directory")

    def name(self) -> str:
        return "cd"


class Exit(Command):
    def run(self, args: str):
        sys.exit(0)

    def name(self) -> str:
        return "exit"


class Type(Command):
    def __init__(self, registry: BuiltinRegistry):
        self.registry = registry

    def run(self, args):
        if self.registry.is_builtin(args):
            print(f"{args} is a shell builtin")
        else:
            path = _cmd_locator(args)
            if path:
                print(f"{args} is {path}")
            else:
                print(f"{args}: not found")

    def name(self) -> str:
        return "type"


class BuiltinRegistry:
    def __init__(self):
        self._commands: dict[str, Command] = {}
        self._register_cmds()

    def _register_cmds(self):
        """Registering all the commands specified above"""
        self.register(Exit())
        self.register(Echo())
        self.register(Pwd())
        self.register(Cd())
        self.register(Type(self))

    def register(self, cmd: Command):
        """register builtin cmd"""
        self._commands[cmd.name()] = cmd

    def get(self, name: str) -> Command | None:
        return self._commands.get(name)

    def is_builtin(self, name: str) -> bool:
        return name in self._commands

    def list_commands(self) -> list[str]:
        """List all registered builtin commands."""
        return list(self._commands.keys())
