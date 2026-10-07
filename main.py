import argparse
import shlex


class Emulator:
    def __init__(self, vfs_path, script_path):
        self.vfs_path = vfs_path
        self.script_path = script_path
        self.vfs_name = "vfs"

    def parse_command(self, line):
        try:
            return shlex.split(line)
        except ValueError:
            print("Ошибка: неверные кавычки")
            return []

    def run_command(self, args):
        if not args:
            return True

        command = args[0]
        values = args[1:]

        if command == "exit":
            return False
        if command == "ls":
            print("ls", *values)
        elif command == "cd":
            print("cd", *values)
        else:
            print("Ошибка: неизвестная команда")

        return True

    def run_script(self):
        try:
            with open(self.script_path, encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue

                    print(f"{self.vfs_name}$ {line}")

                    if not self.run_command(self.parse_command(line)):
                        break
        except FileNotFoundError:
            print("Ошибка: стартовый скрипт не найден")

    def run(self):
        print(f"vfs_path={self.vfs_path}")
        print(f"script_path={self.script_path}")

        if self.script_path:
            self.run_script()

        while True:
            try:
                line = input(f"{self.vfs_name}$ ")
            except EOFError:
                break

            args = self.parse_command(line)

            if not self.run_command(args):
                break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs", required=True)
    parser.add_argument("--script")

    args = parser.parse_args()

    emulator = Emulator(args.vfs, args.script)
    emulator.run()


if __name__ == "__main__":
    main()