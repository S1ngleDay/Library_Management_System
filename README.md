# Library Management System

Простая программа для учета книг. Интерфейс сделан на Python и Tkinter.

## Установка и запуск

Нужен Python 3.10 или новее. Сторонние библиотеки не используются.

```bash
git clone https://github.com/S1ngleDay/Library_Management_System.git
cd Library_Management_System
python3 -m venv .venv
source .venv/bin/activate
python3 main.py
```

В Windows команды `python3` и `source` нужно заменить на соответствующие команды PowerShell. Tkinter обычно уже входит в установщик Python. В Ubuntu или Debian его можно установить отдельно:

```bash
sudo apt install python3-tk
```

Программа умеет искать книги, выдавать и возвращать их, добавлять пользователей и книги, а также показывать историю выдачи.

## Файл с книгами

Список книг находится в `books.txt`. Одна строка — одна книга:

```text
ISBN;Название;Автор
```

Файл должен лежать в корне проекта.
