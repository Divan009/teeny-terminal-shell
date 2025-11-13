from app.cmd_exec import CmdExec


def main():
    executor = CmdExec()

    while True:
        try:
            input_line = input("$ ")
        except EOFError:
            break  # exit gracefully on Ctrl+D
        except KeyboardInterrupt:
            print()  # move to new line on Ctrl+C
            continue

        exit_code = executor.execute(input_line)
        # return exit_code


if __name__ == "__main__":
    main()
