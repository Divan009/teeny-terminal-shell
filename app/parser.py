class CmdParser:
    def parse_cmd(self, input_line: str) -> tuple[str, str]:
        if not input_line.strip():
            return 0

        cmd, *rest = input_line.split(" ", 1)
        args = rest[0] if rest else ""

        return cmd, args