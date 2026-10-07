import os
import shlex


VFS_NAME = "vfs"


def parse_command(line):
    try:
        return shlex.split(line)
    except ValueError:
        print("Ошибка: неверные кавычки")
        return []


def command_ls(args):
    if args:
        print("ls", *args)
    else:
        print("ls")


def command_cd(args):
    if args:
        print("cd", *args)
    else:
        print("cd")


def run_command(args):
    if not args:
        return True

    command = args[0]
    values = args[1:]

    if command == "exit":
        return False
    if command == "ls":
        command_ls(values)
    elif command == "cd":
        command_cd(values)
    else:
        print("Ошибка: неизвестная команда")

    return True


def main():
    while True:
        line = input(f"{VFS_NAME}$ ")
        args = parse_command(line)

        if not run_command(args):
            break


if __name__ == "__main__":
    main()