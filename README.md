# Эмулятор командной оболочки

Эмулятор командной оболочки с виртуальной файловой системой (VFS), реализованный на Python.

## Возможности

- интерактивный режим работы;
- запуск команд из стартового скрипта;
- виртуальная файловая система в формате XML;
- переход между директориями;
- просмотр содержимого VFS;
- отображение дерева файлов и папок;
- просмотр содержимого файлов;
- создание папок;
- копирование файлов;
- вывод календаря;
- обработка ошибок команд и аргументов.

## Поддерживаемые команды

| Команда | Описание |
|---|---|
| `ls` | Показать содержимое текущей папки |
| `cd <папка>` | Перейти в папку |
| `cd ..` | Перейти на уровень выше |
| `tree` | Показать дерево VFS |
| `head <файл>` | Показать первые строки файла |
| `cal` | Показать календарь текущего месяца |
| `cal <месяц> <год>` | Показать календарь указанного месяца |
| `mkdir <папка>` | Создать папку |
| `cp <файл> <копия>` | Скопировать файл |
| `exit` | Завершить работу |

## Пример использования

Ниже приведён пример одной интерактивной сессии, демонстрирующей работу всех основных команд:

```text
shell> ls
home
readme.txt

shell> tree
home
    student
        documents
            hello.txt
readme.txt

shell> cd home
shell> cd student

shell> ls
documents

shell> cd documents

shell> ls
hello.txt

shell> head hello.txt
Hello from VFS

shell> cd ..

shell> mkdir test
shell> ls
documents
test

shell> cd test
shell> cd ..

shell> cp ../readme.txt readme_copy.txt
Ошибка: файл не найден

shell> cd ..
shell> cp readme.txt readme_copy.txt

shell> ls
home
readme.txt
readme_copy.txt

shell> tree
home
    student
        documents
            hello.txt
readme.txt
readme_copy.txt

shell> cal
     October 2026
Mo Tu We Th Fr Sa Su
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31

shell> cal 10 2026
     October 2026
Mo Tu We Th Fr Sa Su
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31

shell> cd home
shell> cd student
shell> cd ..
shell> cd ..

shell> exit