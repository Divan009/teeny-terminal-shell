from __future__ import annotations

import os
import sys
from pathlib import Path

from app.utils import ext_cmd_locator


class Command:
    def run(self, args: list[str]):
        raise NotImplementedError

    def name(self) -> str:
        raise NotImplementedError


class Echo(Command):
    def run(self, args: list[str]):
        print(" ".join(args))

    def name(self) -> str:
        return "echo"


class Pwd(Command):
    def run(self, args: list[str]):
        print(os.getcwd())

    def name(self) -> str:
        return "pwd"


class Cd(Command):
    def run(self, args: list[str]):

        if not args or args[0] == "~":
            target = Path.home()
        else:
            target = Path(" ".join(args))

        try:
            os.chdir(target)
        except FileNotFoundError as e:
            print(f"cd: {target}: No such file or directory")

    def name(self) -> str:
        return "cd"


class Exit(Command):
    def run(self, args: list[str]):
        sys.exit(0)

    def name(self) -> str:
        return "exit"


class History(Command):
    def run(self, args: list[str]):
        sys.exit(0)

    def name(self) -> str:
        return "history"


class Type(Command):
    def __init__(self, registry: BuiltinRegistry):
        self.registry = registry

    def run(self, args: list[str]):
        if not args:
            return

        name = args[0]

        if self.registry.is_builtin(name):
            print(f"{name} is a shell builtin")
        else:
            path = ext_cmd_locator(name)
            if path:
                print(f"{name} is {path}")
            else:
                print(f"{name}: not found")

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
        self.register(History())
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
