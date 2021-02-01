# С этого файла начинается выполнение программы
from sys import argv
import os
import tests


# Функция проверяет наличие параметров, переданных программе
# Возвращает адрес корневой директории в случае успеха
def get_program_args():
    if len(argv) == 2:
        return argv[1]
    else:
        print("Передайте адрес на корневую директорию тестов")
        exit(0)


# Рекурсивная функция, формирует адреса директорий
# param[in] root_folder - корневая папка
# param[in] deep - уровень вложенности папок для тестирования
# return - список адресов к тестируемым директориям
def gen_folders_path(root_folder, deep):
    result = []
    if deep > 0:
        for localDir in os.listdir(root_folder):
            result += gen_folders_path(os.path.join(root_folder, localDir), deep - 1)
        return result
    else:
        for localDir in os.listdir(root_folder):
            result.append(os.path.normpath(os.path.join(root_folder, localDir)))
        return result


# Функция отправляет директории на тестирования,
# анализирует результаты, выводит данные в лог
# param[in] folder_list - список тестируемых директорий
def distribution_folders_to_test(root_folder, folder_list):
    for folder_path in folder_list:
        os.chdir(folder_path)
        print("Тестируется папка: " + folder_path)
        tests.test_folder()
        os.chdir(root_folder)


# Начало выполнения программы
os.chdir(get_program_args())
folders_list = sorted(gen_folders_path(".", 1))
distribution_folders_to_test(get_program_args(), folders_list)