import os
import subprocess

from app.builtins import BuiltinRegistry
from app.history import HistoryStore
from app.utils import ext_cmd_locator


class CmdExec:
    """
    Command Executor will execute command
    """
    registry: BuiltinRegistry

    def __init__(self, history_store: HistoryStore) -> None:
        self.registry = BuiltinRegistry(history_store)

    def execute(self, cmd: str, args: list[str]) -> int:
        if self.registry.is_builtin(cmd):
            builtin_cmd = self.registry.get(cmd)
            return builtin_cmd.run(args)

        return self._run_ext_cmd(cmd, args)

    def execute_pipeline(self, cmds: list[tuple[str, list[str]]]):
        if len(cmds) <= 1:
            return

        prev_read_fd = None
        pids: list[int] = []

        for i, (cmd, args) in enumerate(cmds):
            is_last: bool = (i == len(cmds) - 1)
            if not is_last:
                curr_read_fd, curr_write_fd = os.pipe()
                pid = self._fork_child(cmd, args, prev_read_fd, curr_write_fd)
                if prev_read_fd is not None:
                    os.close(prev_read_fd)

                prev_read_fd = curr_read_fd
                os.close(curr_write_fd)
            else:
                pid = self._fork_child(cmd, args, prev_read_fd, None)
                if prev_read_fd is not None:
                    os.close(prev_read_fd)

            if pid is not None:
                pids.append(pid)

        for pid in pids:
            os.waitpid(pid, 0)


    def _fork_child(self, cmd, args, read_fd, write_fd) -> int:

        pid = os.fork()

        if pid == 0: # child
            if write_fd is not None:
                os.dup2(write_fd, 1)  # stdout -> pipe write
                os.close(write_fd)
            if read_fd is not None:
                os.dup2(read_fd, 0) # stdin -> pipe read
                os.close(read_fd)  # close unused

            if self.registry.is_builtin(cmd):
                self.registry.get(cmd).run(args)
                os._exit(0)
            else:
                try:
                    os.execvp(cmd, [cmd] + args)
                except FileNotFoundError:
                    print(f"{cmd}: command not found")
                    os._exit(1)  # if exec fails
        return pid


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
