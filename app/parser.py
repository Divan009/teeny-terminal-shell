from typing import Any


class CmdParser:
    def parse_input(self, input_line: str) -> int | tuple[str, list[str] | Any]:
        if not input_line.strip():
            return 0

        cmd, *rest = input_line.split(" ", maxsplit=1)
        args: str | Any = rest[0] if rest else ""

        args: list[str] = self.parse_args(args) if args else []

        return cmd, args

    def parse_args(self, args: str | None):
        if args is None:
            return None

        current = ""
        in_single_quote = False
        in_double_quote = False

        result = []

        i = 0

        while i < len(args):

            if args[i] == "'" and not in_double_quote:
                in_single_quote = not in_single_quote

            elif args[i] == '"' and not in_single_quote:
                in_double_quote = not in_double_quote

            elif args[i].isspace() and not in_single_quote and not in_double_quote:
                if current != "":
                    result.append(current)
                    current = ""
            else:
                # if args[i] != "'":
                current += args[i]
            i += 1

        # Add final token
        if current != "":
            result.append(current)

        return result
