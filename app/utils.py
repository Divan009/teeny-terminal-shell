import os
import stat
from os import stat_result
from typing import Any



def _cmd_locator(cmd: str) -> str | None:
    path: str | None = os.getenv("PATH")
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


def custom_completer(text, state) -> Any | None:
    from app.builtins import BuiltinRegistry

    all_cmds_registery = BuiltinRegistry()

    options = all_cmds_registery.list_commands()
    matches = [s for s in options if s.startswith(text)]

    if state < len(matches):
        return matches[state] + " "
    return None
