import os
import stat
from os import stat_result
from typing import Any


_EXTERNAL_COMMANDS: list[str] | None = None

def ext_cmd_locator(cmd: str) -> str | None:
    """
    Given a command name, try to locate an executable file with that name
    in the PATH. Returns the full path or None if not found.
    """

    path: str | None = os.getenv("PATH")
    if not path:
        return None

    potential_dir: list[str] = path.split(":")

    for dir in potential_dir:
        filenames: list[str]
        dirnames: list[str]
        dirpath: str
        for dirpath, dirnames, filenames in os.walk(dir):
            for filename in filenames:
                if filename == cmd:
                    try:
                        filepath = os.path.join(dirpath, filename)

                        file_stat: stat_result = os.stat(filepath)
                        mode: int = file_stat.st_mode
                        if (
                            mode & stat.S_IXUSR
                            or mode & stat.S_IXGRP
                            or mode & stat.S_IXOTH
                        ):
                            return filepath
                    except OSError as e:
                        print(f"Error accessing {filepath}: {e}")
    return None


def find_all_ext_cmd_in_path() -> list[str]:
    """
    Given the path, find all executable commands in it
    :return:
    """
    path: str | None = os.getenv("PATH")

    global _EXTERNAL_COMMANDS
    if _EXTERNAL_COMMANDS is not None:
        return _EXTERNAL_COMMANDS

    potential_dir: list[str] = path.split(":")
    external_cmds_set: set[str] = set()

    for dir in potential_dir:
        if not dir:
            continue

        try:
            entries = os.listdir(dir)
        except OSError:
            continue

        for filename in entries:
            filepath = os.path.join(dir, filename)
            try:
                file_stat: stat_result = os.stat(filepath)
            except OSError:
                continue

            mode: int = file_stat.st_mode
            if (
                mode & stat.S_IXUSR
                or mode & stat.S_IXGRP
                or mode & stat.S_IXOTH
            ):
                external_cmds_set.add(filename)

    _EXTERNAL_COMMANDS = list(external_cmds_set)
    return _EXTERNAL_COMMANDS

def custom_completer(text, state) -> Any | None:
    from app.builtins import BuiltinRegistry

    all_cmds_registry = BuiltinRegistry()
    external_commands = find_all_ext_cmd_in_path()
    builtin_commands = all_cmds_registry.list_commands()

    options = sorted(set(external_commands + builtin_commands))
    matches = [s for s in options if s.startswith(text)]

    if state >= len(matches):
        return None

    if len(matches) == 1:
        return matches[0] + " "

    return matches[state]
