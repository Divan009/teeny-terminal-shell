import os
import readline
from typing import Any

from app.cmd_exec import CmdExec
from app.parser import CmdParser
from app.utils import custom_completer


class Shell:
    executor: CmdExec
    parser: CmdParser

    def __init__(self):
        self.running = True
        self.parser = CmdParser()
        self.executor = CmdExec()

        readline.set_completer(custom_completer)
        readline.parse_and_bind("tab: complete")

    def run_shell(self):
        while self.running:
            try:
                result = self._parse_user_input()
                if result is None:
                    continue

                cmd, args = result

                if cmd:
                    self.executor.execute(cmd, args)
            except KeyboardInterrupt:
                print()
                break

    def _parse_user_input(self) -> int | tuple[str, list[str] | Any] | None:
        PROMPT: str = "$ "

        try:
            input_line = input(PROMPT)

            if input_line == "":
                self.running = False
                return None

            input_line = input_line.strip()

            # Empty line: just ignore and reprompt
            if not input_line:
                return None

            if ">" in input_line:
                os.system(input_line)
                return None

            return self.parser.parse_input(input_line)
        except (EOFError, KeyboardInterrupt):
            # Also handle EOFError just in case
            self.running = False
            return None


def main():
    shell = Shell()
    shell.run_shell()


if __name__ == "__main__":
    main()
