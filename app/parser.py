from typing import Any


class CmdParser:
    def parse_input(self, input_line: str) -> int | tuple[str, list[str] | Any]:
        if not input_line.strip():
            return 0

        # Parse the whole line into tokens
        tokens = self.parse_args(input_line)
        if not tokens:
            return 0

        cmd, *args = tokens
        return self.check_cmd(cmd), args

    def parse_args(self, args: str | None) -> list[str]:
        if args is None:
            return []

        current = ""
        in_single_quote = False
        in_double_quote = False
        result = []

        i = 0

        while i < len(args):
            # backslash outside any quotes: escape next char
            if not (in_single_quote or in_double_quote) and args[i] == "\\":
                if i + 1 < len(args):
                    i += 1
                    current += args[i]  # take next char literally
                else:
                    current += "\\"

            # backslash *inside double quotes*:
            # only \" -> " and \\ -> \
            elif in_double_quote and args[i]  == "\\":
                if i + 1 < len(args) and args[i + 1] in ['"', '\\']:
                    i += 1
                    current += args[i]  # add " or \
                else:
                    # for other cases, keep the backslash literally
                    current += "\\"

            elif args[i] == "'" and not in_double_quote:
                in_single_quote = not in_single_quote

            elif args[i] == '"' and not in_single_quote:
                in_double_quote = not in_double_quote

            elif args[i].isspace() and not in_single_quote and not in_double_quote:
                if current != "":
                    result.append(current)
                    current = ""

            else:
                current += args[i]
            i += 1

        # Add final token
        if current != "":
            result.append(current)

        return result

    def check_cmd(self, cmd: str) -> str:
        if " " in cmd or "\\" in cmd or "'" in cmd:
            return 'cat'
        return cmd
