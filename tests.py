import os
import re


# Функция тестирует папку и выводит ошибки в местный файл лога
# return - результат тестирования True/False
def test_folder():
    open("report.txt", "w").close()     # инициализация лог файла
    test_1_result = test_check_exist_folders(["ft_reference", "ft_run"])
    if test_1_result:
        add_to_log("directory missing: " + ' '.join(test_1_result))
        return False
    ft_run_not_files, ft_run_extra_files = test_identity_files("ft_reference", "ft_run", r'\.stdout$')
    result = True
    if ft_run_not_files:
        add_to_log("In ft_run there are missing files present in ft_reference: " +
                   ', '.join(list(map(lambda x: "'" + x + "'", ft_run_not_files))))
        result = False
    if ft_run_extra_files:
        add_to_log("In ft_run there are extra files not present in ft_reference: " +
                   ', '.join(list(map(lambda x: "'" + x + "'", ft_run_extra_files))))
        result = False
    if not result:
        return False
    # test_3_errors - имя файла, номер строки, строка с ошибкой
    # test_4_mem - имя файла, mem_max, bricks_last
    # test_4_bricks - имя файла, mem_max, bricks_last
    is_solver, test_3_errors, test_4_mem, test_4_bricks = check_files("ft_reference", "ft_run")
    for error in test_3_errors:
        add_to_log("{}({:d}): {}".format(error[0], error[1], error[2].rstrip()))
        result = False
    for error in is_solver:
        add_to_log("{}: missing 'Solver finished at'".format(error))
        result = False
    for error in test_4_mem:
        add_to_log("{}: different 'Memory Working Set Peak' "
                   "(ft_run={:.1f}, ft_reference={:.2f}, rel.diff={:.2f}, criterion={:d})"
                   "".format(error[0], error[1], error[2], error[3], 4))
        result = False
    for error in test_4_bricks:
        add_to_log("{}: different 'Total' of bricks "
                   "(ft_run={:d}, ft_reference={:d}, rel.diff={:.2f}, criterion={:.1f})"
                   "".format(error[0], error[1], error[2], error[3], 0.1))
        result = False
    return result


def add_to_log(text):
    with open("report.txt", "a") as file:
        file.write(text + "\n")


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
    test_3_is_solver = []       # имя файла
    test_3_errors = []          # имя файла, номер строки, строка с ошибкой
    test_4_ft_run = []          # имя файла, mem_max, bricks_last
    test_4_ft_reference = []    # имя файла, mem_max, bricks_last

    # анализ папки ft_run
    ft_run_files = files_in_folder(ft_run)
    saved_dir = os.getcwd()
    os.chdir(ft_run)
    for file in ft_run_files:
        is_solver, errors, mem_max, bricks_last = check_file_lines(file, True, True if re.findall(r'\.stdout$', file) else False)
        if is_solver:
            test_3_is_solver.append(file)
        for error in errors:
            test_3_errors.append([file] + error)
        test_4_ft_run.append([file, mem_max, bricks_last])
    # очистка списка от файлов не .stdout
    test_4_ft_run = list(filter(lambda x: re.findall(r'\.stdout$', x[0]), test_4_ft_run))
    os.chdir(saved_dir)
    # анализ папки ft_reference
    ft_reference_files = files_in_folder(ft_reference)
    os.chdir(ft_reference)
    for file in ft_reference_files:
        _, _, mem_max, bricks_last = check_file_lines(file, False, True if re.findall(r'\.stdout$', file) else False)
        test_4_ft_reference.append([file, mem_max, bricks_last])
    os.chdir(saved_dir)
    comp_results(test_4_ft_reference, test_4_ft_run)
    test_4_mem, test_4_bricks = comp_results(test_4_ft_reference, test_4_ft_run)
    return test_3_is_solver, test_3_errors, test_4_mem, test_4_bricks


# ф-я для расчёта значений теста 4
def comp_results(test_4_ft_reference, test_4_ft_run):
    test_4_mem = []     # ft_run, ft_ref, коэфициент, реальная разница
    test_4_bricks = []
    for i in range(len(test_4_ft_run)):
        mem_values = [test_4_ft_reference[i][1], test_4_ft_run[i][1]]
        if max(mem_values) / min(mem_values) > 5:
            test_4_mem.append([test_4_ft_run[i][0],                                             # файл
                               test_4_ft_run[i][1], test_4_ft_reference[i][1],                  # значения
                               calcRelDiff(test_4_ft_run[i][1], test_4_ft_reference[i][1])])    # реальная разница
        bricks_values = [test_4_ft_reference[i][2], test_4_ft_run[i][2]]
        brick_max = float(max(bricks_values))
        brick_min = float(min(bricks_values))
        if (brick_max - brick_min) / brick_min > 0.1:
            test_4_bricks.append([test_4_ft_run[i][0],                                          # файл
                                  test_4_ft_run[i][2], test_4_ft_reference[i][2],               # значения
                                  calcRelDiff(test_4_ft_run[i][2], test_4_ft_reference[i][2])]) # реальная разница
    return test_4_mem, test_4_bricks


# функция анализа файла по строкам
# param[in] is_ft_run - файл из каталога ft_run?
# param[in] is_stdout - файл типа .stdout?
# Возвращаемые значения:
#   is_solver       - наличие строки с 'Solver finished at'
#   errors_list     - список ошибок теста 3
#   max(mem_res)    - максимальное значение mem
#   bricks_res      - последнее значение bricks
def check_file_lines(file_path, is_ft_run, is_stdout):
    is_solver = False           # указывает на наличие строки 'Solver finished at'
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
            if re.match(r'Solver finished at', logLine):
                is_solver = True
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
    return not is_solver, errors_list, max(mem_res), bricks_res


# ф-я для рассчёта реальной разницы
def calcRelDiff(a, b):
    return (max(a, b) - min(a, b)) / min(a, b)