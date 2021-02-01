# С этого файла начинается выполнение программы
import TestFunctions
from sys import argv


# Функция проверяет наличие параметров, переданных программе и возвращает адрес корневой директории в случае успеха
def getProgArgs():
    if len(argv) == 2:
        return argv[1]
    else:
        print("Передайте адрес на корневую директорию тестов")
        exit(0)


# Точка старта программы
TestFunctions.startTests(getProgArgs(), 1)
