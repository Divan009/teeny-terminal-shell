import os
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

    def execute_pipeline(self, cmds: list[tuple[str, list[str]]]):
        """
        # pipeline: list[(cmd, args)] = [('cat', ['/tmp/foo/file']), ('wc', [])]
        :param cmds:
        :return:
        """
        if len(cmds) != 2:
            print("Only two-command pipelines supported")
            return None

        (cmd1, args1), (cmd2, args2) = cmds

        read_fd, write_fd = os.pipe()

        pid1 = os.fork()

        if pid1 == 0: # child
            os.dup2(write_fd, 1)  # stdout -> pipe write
            os.close(read_fd)  # close unused
            os.close(write_fd)
            os.execvp(cmd1, [cmd1] + args1)
            sys.exit(1)  # if exec fails

        # Fork for second command (right side)
        pid2 = os.fork()
        if pid2 == 0:
            os.dup2(read_fd, 0)
            os.close(read_fd)
            os.close(write_fd)
            os.execvp(cmd2, [cmd2] + args2)
            sys.exit(1)

        # Parent
        os.close(write_fd)
        os.close(read_fd)

        # Wait for both children
        os.waitpid(pid1, 0)
        os.waitpid(pid2, 0)


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
