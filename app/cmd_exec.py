import subprocess

from app.builtins import BuiltinRegistry
from app.utils import ext_cmd_locator


class CmdExec:
    """
    Command Executor will execute command
    """
    registry: BuiltinRegistry

    def __init__(self) -> None:
        self.registry = BuiltinRegistry()

    def execute(self, cmd: str, args: list[str]) -> int:
        if self.registry.is_builtin(cmd):
            builtin_cmd = self.registry.get(cmd)
            return builtin_cmd.run(args)

        return self._run_ext_cmd(cmd, args)

    def _run_ext_cmd(self, cmd: str, args: list[str]):
        """
        :type args: str
        :type cmd: str
        """

        # Split args into list for subprocess
        filepath = ext_cmd_locator(cmd)

        if args is None:
            args = []

        if not filepath:
            print(f"{cmd}: command not found")
            return 127

        try:
            argv = [cmd] + args
            subprocess.run(argv, executable=filepath)
        except PermissionError:
            print(f"{cmd}: permission denied")
            return 126
        except Exception as e:
            print(f"Error executing {cmd}: {e}")
            return 1
