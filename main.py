import argparse
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
            node = self.get_current_node()

            for child in node:
                print(child.get("name"))

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