import os
import readline

from app.cmd_exec import CmdExec
from app.history import HistoryStore
from app.parser import CmdParser
from app.utils import custom_completer


class Shell:
    """
    reads line, handles Ctrl+C / EOF, maybe basic checks.
    """
    executor: CmdExec
    parser: CmdParser
    Command = tuple[str, list[str]]

    def __init__(self):
        self.running = True
        self.parser = CmdParser()
        self.history = HistoryStore()
        self.executor = CmdExec(self.history)

        readline.set_completer(custom_completer)
        readline.parse_and_bind("tab: complete")


    def run_shell(self):
        while self.running:
            try:
                result = self._parse_user_input()

                if result is None:
                    continue

                if isinstance(result, list):
                    self.executor.execute_pipeline(result)
                else:
                    cmd, args = result
                    self.executor.execute(cmd, args) # single command: (cmd, args)
            except KeyboardInterrupt:
                print()
                break

    def _parse_pipeline_cmd(self, input_lines: list[str]):
        all_input = []
        for input_line in input_lines:
            result = self.parser.parse_input(input_line)
            if result is None:
                continue
            all_input.append(result)
        return all_input


    def _parse_user_input(self) -> Command | None | list[Command]:
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

            self.history.add(input_line)

            if ">" in input_line:
                os.system(input_line)
                return None

            if "|" in input_line:
                input_line = input_line.split("|") # ['cat /tmp/foo/file ', ' wc']
                return self._parse_pipeline_cmd(input_line)

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
