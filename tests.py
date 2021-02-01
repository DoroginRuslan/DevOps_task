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
    for i in check_files("ft_reference", "ft_run"):
        print('file: "{}" line number: {:d}, text: "{}"'.format(i[0], i[1], i[2].rstrip()))


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
                res_address.append(os.path.normpath(file_address))
    os.chdir(saved_path)
    return res_address


# функция запускает построчное тестирование файлов из папки
def check_files(ft_reference, ft_run):
    test_3_errors = []          # имя файла, номер строки, строка с ошибкой
    test_4_ft_run = []          # имя файла, mem_max, bricks_last
    test_4_ft_reference = []    # имя файла, mem_max, bricks_last

    # анализ папки ft_run
    ft_run_files = files_in_folder(ft_run)
    saved_dir = os.getcwd()
    os.chdir(ft_run)
    for file in ft_run_files:
        errors, mem_max, bricks_last = check_file_lines(file, True, True if re.findall(r'\.stdout$', file) else False)
        for error in errors:
            test_3_errors.append([file] + error)
        test_4_ft_run.append([file, mem_max, bricks_last])
    test_4_ft_run = [_ if re.findall(r'\.stdout$', _) for _ in test_4_ft_run]

    os.chdir(saved_dir)
    # анализ папки ft_reference
    ft_reference_files = files_in_folder(ft_reference)
    os.chdir(ft_reference)
    for file in ft_reference_files:
        _, mem_max, bricks_last = check_file_lines(file, False, True if re.findall(r'\.stdout$', file) else False)
        test_4_ft_reference.append([file, mem_max, bricks_last])
    os.chdir(saved_dir)
    return test_3_errors


# поиск
def find_different_test_4(test_4_ft_run, test_4_ft_reference):



# функция анализа файла по строкам
# param[in] is_ft_run - файл из каталога ft_run?
# param[in] is_stdout - файл типа .stdout?
def check_file_lines(file_path, is_ft_run, is_stdout):
    errors_list = []            # список для сохранения строк со словом error
    mem_res = []                # значения для строк с "Memory Working Set Peak"
    regex_line_mem = r'Memory Working Set Current = [\d\.]+ Mb, Memory Working Set Peak = [\d\.]+ Mb'
    bricks_res = None           # последнее значение для строк с "MESH::Bricks"
    regex_line_bricks = r'MESH::Bricks: Total=[\d\.]+ Gas=[\d\.]+ Solid=[\d\.]+ Partial=[\d\.]+ Irregular=[\d\.]+'
    file_data = open(file_path, "r")
    line_number = 0
    for logLine in file_data:
        line_number += 1
        # Поиск строк со словом Error из каталога ft_run
        if is_ft_run:
            if re.findall(r'\berror\b', logLine, re.IGNORECASE):
                errors_list.append([line_number, logLine])
        # Тесты для файлов .stdout
        if is_stdout:
            # Поиск данных памяти
            mem_format_line = re.findall(regex_line_mem, logLine)
            if mem_format_line:
                mem_res.append(float(re.findall(r'[\d\.]+', mem_format_line[0])[1]))
            # Поиск данных Bricks
            bricks_format_line = re.findall(regex_line_bricks, logLine)
            if bricks_format_line:
                bricks_res = int(re.findall(r'[\d\.]+', bricks_format_line[0])[0])
    return errors_list, max(mem_res), bricks_res

