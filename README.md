# Mini POSIX Shell

A small POSIX-style shell implemented in Python as part of the Codecrafters “Build Your Own Shell” challenge. It supports basic job control primitives, builtins, pipelines, tab completion and a history system with file persistence via `HISTFILE`.

---

## Features

* **External commands**

  * Resolves commands using `$PATH`.
  * Uses `os.fork` + `os.execvp`, with a `command not found` message when resolution fails.

* **Pipelines**

  * Supports `cmd1 | cmd2 | cmd3` using `os.pipe` to wire `stdin`/`stdout` between processes.

* **Builtins**

  * `echo`, `pwd`, `cd`, `exit`, `type`, `history`.
  * `type` reports whether a name is a builtin or an external command (and its path if found).

* **History**

  * In-memory history stored via a `HistoryStore` object.
  * Commands are recorded before execution, including `history` itself.
  * `history` – print all commands.
  * `history N` – print the last N commands.
  * `history -r <file>` – read and append commands from a history file.
  * `history -w <file>` – write full in-memory history to a file (truncate).
  * `history -a <file>` – append only commands executed since the last `-a`/`-w`.

* **HISTFILE support**

  * On startup: if `HISTFILE` is set, history is loaded from that file.
  * On exit: if `HISTFILE` is set, in-memory history is written back to that file.

* **Tab completion**

  * Uses `readline` to complete builtin names and executables found in `$PATH`.

---

## Architecture (high-level)

* `Shell`
  REPL loop: reads lines, records them in `HistoryStore`, then delegates parsing/execution.

* `CmdExec`
  Knows how to run builtins (via a `BuiltinRegistry`) or external commands, and how to build pipelines.

* `BuiltinRegistry`
  Registers builtin commands and injects shared dependencies (like `HistoryStore`) into them.

* `HistoryStore`
  Wraps a simple `list[str]` and provides helpers for loading/saving/appending history.

This keeps state (history), parsing, and execution separated, and avoids global singletons in favor of explicit wiring.

---

## Running

Requirements: Python 3.10+

```bash
./your_program.sh
# or
python -m app.main
```

Optional persistent history:

```bash
export HISTFILE=/tmp/shell_history.txt
./your_program.sh
```

---

## Example

```bash
$ echo hello world
hello world
$ pwd
/home/user
$ ls | grep ".py"
main.py
$ history 3
    3  pwd
    4  ls | grep ".py"
    5  history 3
```
