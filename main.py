import argparse
import calendar
from datetime import datetime
import shlex
import xml.etree.ElementTree as ET


class Emulator:
    def __init__(self, vfs_path):
        self.vfs_path = vfs_path
        self.vfs = None
        self.current_path = []
        self.load_vfs()

    def load_vfs(self):
        try:
            tree = ET.parse(self.vfs_path)
            self.vfs = tree.getroot()

        except FileNotFoundError:
            print("Ошибка: VFS-файл не найден")
            raise SystemExit

        except ET.ParseError:
            print("Ошибка: неправильный формат VFS")
            raise SystemExit

    def get_current_node(self):
        node = self.vfs

        for name in self.current_path:
            found = None

            for child in node:
                if child.tag == "folder" and child.get("name") == name:
                    found = child
                    break

            if found is None:
                return None

            node = found

        return node

    def execute(self, command_line):
        try:
            args = shlex.split(command_line)
        except ValueError:
            print("Ошибка: неправильные кавычки")
            return True

        if not args:
            return True

        command = args[0]

        if command == "exit":
            return False

        elif command == "ls":
            if len(args) != 1:
                print("Ошибка: неверные аргументы")
                return True

            node = self.get_current_node()

            for child in node:
                print(child.get("name"))

        elif command == "tree":
            if len(args) != 1:
                print("Ошибка: неверные аргументы")
                return True

            node = self.get_current_node()

            def print_tree(current_node, level):
                for child in current_node:
                    print("    " * level + child.get("name"))

                    if child.tag == "folder":
                        print_tree(child, level + 1)

            print_tree(node, 0)

        elif command == "head":
            if len(args) != 2:
                print("Ошибка: неверные аргументы")
                return True

            file_name = args[1]
            node = self.get_current_node()

            found = None

            for child in node:
                if child.tag == "file" and child.get("name") == file_name:
                    found = child
                    break

            if found is None:
                print("Ошибка: файл не найден")
                return True

            text = found.text or ""
            lines = text.splitlines()

            for line in lines[:10]:
                print(line)

        elif command == "cal":
            if len(args) == 1:
                now = datetime.now()
                print(calendar.month(now.year, now.month))

            elif len(args) == 3:
                try:
                    month = int(args[1])
                    year = int(args[2])

                    if month < 1 or month > 12:
                        print("Ошибка: неверный месяц")
                        return True

                    print(calendar.month(year, month))

                except ValueError:
                    print("Ошибка: неверные аргументы")

            else:
                print("Ошибка: неверные аргументы")

        elif command == "cd":
            if len(args) != 2:
                print("Ошибка: неверные аргументы")
                return True

            path = args[1]

            if path == "..":
                if self.current_path:
                    self.current_path.pop()
                return True

            node = self.get_current_node()

            for child in node:
                if child.tag == "folder" and child.get("name") == path:
                    self.current_path.append(path)
                    return True

            print("Ошибка: папка не найдена")

        else:
            print("Ошибка: неизвестная команда")

        return True


def run_script(emulator, script_path):
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                print("shell>", line)

                if not emulator.execute(line):
                    break

    except FileNotFoundError:
        print("Ошибка: стартовый скрипт не найден")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--vfs", required=True)
    parser.add_argument("--script")

    args = parser.parse_args()

    emulator = Emulator(args.vfs)

    if args.script:
        run_script(emulator, args.script)
    else:
        while True:
            try:
                line = input("shell> ")

                if not emulator.execute(line):
                    break

            except EOFError:
                break


if __name__ == "__main__":
    main()