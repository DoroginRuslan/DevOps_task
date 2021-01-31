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
            result.append(os.path.join(root_folder, localDir))
        return result


# Функция отправляет директории на тестирования,
# анализирует результаты, выводит данные в лог
# param[in] folder_list - список тестируемых директорий
def distribution_folders_to_test(folder_list):
    for folder_path in folder_list:
        test_folder(folder_path)


# Функция тестирует папку и выводит ошибки в метсный файл лога
# param[in] - тестируемая директория
# return - результат тестирования True/False
def test_folder(folder_path):
    print("Тестируется папка: " + folder_path)
    test_1 = test_check_exist_folders(folder_path, ["ft_reference", "ft_run"])
    if test_1:
        print("\tОтсутствующие директории: " + ''.join(test_1))


# функция проверяет наличие папок в тестируемой директории
# param[in] folder_path - тестируемая директория
# param[in] list_in_dirs - папки, которые должны находиться внутри тестируемой директории
# return - список отсутсвующих папок
def test_check_exist_folders(folder_path, list_required_dirs):
    result = []
    list_path_dirs = os.listdir(folder_path)
    for required_folder in list_required_dirs:
        if required_folder not in list_path_dirs:
            result.append(required_folder)
    return result


# Начало выполнения программы
folders_list = gen_folders_path(get_program_args(), 1)
distribution_folders_to_test(folders_list)
