import os
from pathlib import Path
import stat
import subprocess


def _cmd_locator(cmd: str):
    path = os.getenv("PATH")
    potential_dir = path.split(":")

    for dir in potential_dir:
        for dirpath, dirnames, filenames in os.walk(dir):
            for filename in filenames:
                if filename == cmd:
                    try:
                        filepath = os.path.join(dirpath, filename)

                        file_stat = os.stat(filepath)
                        mode = file_stat.st_mode
                        if (
                            mode & stat.S_IXUSR
                            or mode & stat.S_IXGRP
                            or mode & stat.S_IXOTH
                        ):
                            return filepath
                    except OSError as e:
                        print(f"Error accessing {filepath}: {e}")
    return None


def _run_ext_cmd(cmd: str, args: str):
    # Split args into list for subprocess
    filepath = _cmd_locator(cmd)
    if not filepath:
        print(f"{cmd}: command not found")

    subprocess.run([filepath], args=args.split())
