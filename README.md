[![progress-banner](https://backend.codecrafters.io/progress/shell/0b83adff-779a-4c34-ad54-f7b354c84351)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

This is a starting point for Python solutions to the
["Build Your Own Shell" Challenge](https://app.codecrafters.io/courses/shell/overview).

In this challenge, you'll build your own POSIX compliant shell that's capable of
interpreting shell commands, running external programs and builtin commands like
cd, pwd, echo and more. Along the way, you'll learn about shell command parsing,
REPLs, builtin commands, and more.

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

# Passing the first stage

The entry point for your `shell` implementation is in `app/main.py`. Study and
uncomment the relevant code, and push your changes to pass the first stage:

```sh
git commit -am "pass 1st stage" # any msg
git push origin master
```

Time to move on to the next stage!

# Stage 2 & beyond

Note: This section is for stages 2 and beyond.

1. Ensure you have `python (3.13)` installed locally
1. Run `./your_program.sh` to run your program, which is implemented in
   `app/main.py`.
1. Commit your changes and run `git push origin master` to submit your solution
   to CodeCrafters. Test output will be streamed to your terminal.


---------

Yes — that article from ZetCode on `os.pipe()` is *very good*, and it covers exactly the low-level building blocks you’ll need for implementing your pipeline support (i.e., the `|` operator for two commands). ([zetcode.com][1])

Let me walk you through how to **interpret that article** and map it to your shell’s needs — that way you understand *why* we’re using pipe/fork/dup2, and you’ll be ready to write the code when you’re ready.

---

## 🔍 What the article covers (in summary)

* `os.pipe()` creates a unidirectional communication channel between two file descriptors: one for reading, one for writing. ([zetcode.com][1])
* Example: parent writes to pipe, child reads from pipe. ([zetcode.com][1])
* Use of `os.fork()` (to create child process). ([zetcode.com][1])
* In child: close unused end of pipe, read/write as required. Parent: close opposite end. ([zetcode.com][1])
* It also shows more advanced topics: two‐way pipes, non‐blocking, `select`, etc. ([zetcode.com][1])

---

## 🧩 How this maps to your shell’s pipeline (`cmd1 | cmd2`)

When you type:

```
cmd1 args1 | cmd2 args2
```

You need to implement:

* A pipe so `stdout` of `cmd1` flows into `stdin` of `cmd2`.
* A fork for `cmd1`.
* A fork for `cmd2`.
* Setup redirections so `cmd1` writes into pipe, and `cmd2` reads from pipe.
* Close unused ends so there are no leaks or hanging processes.
* Parent process waits for children to finish (or handles streaming behavior in `tail -f` case).

The article shows you the pieces:

* `os.pipe()` → gives you two fds: `(read_fd, write_fd)`
* `os.fork()` → spawn children
* In children: use `os.dup2()` (or `os.dup()` then `os.close()`) to redirect `0` (stdin) or `1` (stdout) to the pipe fds
* Then `os.execvp()` (or a variant) to replace the process image with the external command
* Close unused fds
* Parent waits and closes both ends

---

## ✅ What *you* should extract / learn from the article

1. **Understand `os.pipe()` signature and meaning**

   > `r, w = os.pipe()` → `r` is read-end, `w` is write-end.

2. **Understand `os.fork()`**

   > `pid = os.fork()`
   > If `pid > 0`, you’re in parent. If `pid == 0`, you’re in child.

3. **File descriptor management**

   * Child that writes: close `r`, keep `w`
   * Child that reads: close `w`, keep `r`
   * Parent: close both `r` and `w` after forking both children

4. **I/O redirection**

   * Use `os.dup2(old_fd, new_fd)` to make e.g. `stdout` go to `w`
   * Then close original `w` (you no longer need the separate fd)

5. **Exec external commands**

   * Use `os.execvp(cmd, [cmd] + args)` (or similar)
   * After exec, the current process becomes that command; it doesn’t return to your code.

6. **Waiting and cleanup**

   * Parent must `os.waitpid(pid1, 0)` and `os.waitpid(pid2, 0)` so children don’t become zombies.
   * Parent closes the pipe ends so children get EOF when appropriate (important for commands like `head -n 5`).

---

## 🧠 Why it might feel tricky

Because you’re learning several new systems concepts together:

* Processes (`fork`, `exec`)
* Pipes (inter-process communication)
* File descriptor redirection (`dup2`)
* Cleanly closing unused fds to avoid deadlocks
* Integrating the whole thing into your shell architecture (parser + executor)

It’s **okay** that it feels heavy now — part of being senior is breaking it into digestible pieces, and you’re doing that.

---

## 🛠 My suggestion: incremental approach

Here’s how I’d proceed:

1. Write a small **separate script** (not tied to your shell) that does:

   ```python
   import os
   r, w = os.pipe()
   pid = os.fork()
   if pid == 0:
       # child: writes
       os.close(r)
       os.dup2(w, 1)     # redirect stdout to write end
       os.close(w)
       os.execvp("ls", ["ls", "-l"])
   else:
       # parent: reads
       os.close(w)
       data = os.read(r, 1024)
       print("Parent read:", data.decode())
       os.close(r)
       os.waitpid(pid, 0)
   ```

   Run it and verify you see output of `ls`.

2. Then evolve it to two forks and two commands: `cmd1 | cmd2`.

3. Once that works, integrate into `execute_pipeline`.

---

If you like, I can pull up **the exact section** of the ZetCode article that shows parent-child pipe communication and we can walk through **line by line**, relating each line to what you must do for your shell. Would that be helpful?

[1]: https://zetcode.com/python/os-pipe/ "Python os.pipe Function - Complete Guide"
