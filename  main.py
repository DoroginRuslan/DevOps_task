# С этого файла начинается выполнение программы
from sys import argv
import os


# Функция проверяет наличие параметров, переданных программе
# Возвращает адрес корневой директории в случае успеха
def get_program_args():
    if len(argv) == 2:
        return argv[1]
    else:
        print("Передайте адрес на корневую директорию тестов")
        exit(0)


# Рекурсивная функция, формирует адреса папок
# param[in] root_folder - корневая папка
# param[in] deep - уровень вложенности папок для тестирования
# return - список адресов к тестируемым папкам
def gen_folders_path(root_folder, deep):
    result = []
    if deep > 0:
        for localDir in os.listdir(root_folder):
            result += gen_folders_path(os.path.join(root_folder, localDir), deep - 1)
        return result
    else:
        for localDir in os.listdir(root_folder):
            result.append(os.path.join(root_folder, localDir))
        return result


# Начало выполнения программы
for test_path in gen_folders_path(get_program_args(), 1):
    print(test_path)
