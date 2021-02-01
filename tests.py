import os
import re


# Функция тестирует папку и выводит ошибки в местный файл лога
# return - результат тестирования True/False
def test_folder():
    test_1_result = test_check_exist_folders(["ft_reference", "ft_run"])
    if test_1_result:
        print("\tОтсутствующие директории: " + ''.join(test_1_result))
        return False
    ft_run_not_files, ft_run_extra_files = test_identity_files("ft_reference", "ft_run", r'\.stdout$')
    if ft_run_not_files:
        print("In ft_run there are missing files present in ft_reference: " + ''.join(ft_run_not_files))
    if ft_run_extra_files:
        print("In ft_run there are extra files files not present in ft_reference: " + ''.join(ft_run_extra_files))


# функция проверяет наличие папок в тестируемой директории
# param[in] list_in_dirs - папки, которые должны находиться внутри тестируемой директории
# return - список отсутсвующих папок
def test_check_exist_folders(list_required_dirs):
    result = []
    list_path_dirs = os.listdir()
    for required_folder in list_required_dirs:
        if required_folder not in list_path_dirs:
            result.append(required_folder)
    return result


# функция проверяет совпадение имен файлов в папках
# param[in] ft_reference - имя папки
# param[in] ft_run - имя папки
# param[in] mask - маска для адреса
# return - ft_run_not_files - список не найденных файлов в ft_run
#          ft_run_extra_files - список лишних файлов в ft_run
def test_identity_files(ft_reference, ft_run, mask):
    ft_reference_files = files_in_folder(ft_reference, mask)
    ft_run_files = files_in_folder(ft_run, mask)
    ft_run_not_files = []
    for ref_file in ft_reference_files:
        if ref_file not in ft_run_files:
            ft_run_not_files.append(os.path.normpath(ref_file))
    ft_run_extra_files = []
    for run_file in ft_run_files:
        if run_file not in ft_reference_files:
            ft_run_extra_files.append(os.path.normpath(run_file))
    return ft_run_not_files, ft_run_extra_files


# функция выдаёт список относительных файлов в каталоге
# param[in] folder_path - каталог, относительно которого получаем адреса файлов
# param[in] regex_mask - маска файлов
def files_in_folder(folder_path, regex_mask=r'.'):
    res_address = []
    saved_path = os.getcwd()
    os.chdir(folder_path)
    for folder in os.walk("."):
        for fileFolder in folder[2]:
            file_address = os.path.join(folder[0], fileFolder)
            if re.findall(regex_mask, file_address):
                res_address.append(file_address)
    os.chdir(saved_path)
    return res_address
