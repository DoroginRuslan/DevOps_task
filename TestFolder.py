# Файл содержит реализацию класса TestFolder, предназначенного для хранения тестов для папки
from Navigation import Navigation
from Report import Report
import re


# Функция для извлечения чисел из строки
def findMaxSetPeak(logLines):
    mem_res = []
    regex_line_mem = r'Memory Working Set Current = [\d\.]+ Mb, Memory Working Set Peak = [\d\.]+ Mb'
    bricks_res = None
    regex_line_bricks = r'MESH::Bricks: Total=[\d\.]+ Gas=[\d\.]+ Solid=[\d\.]+ Partial=[\d\.]+ Irregular=[\d\.]+'
    for logLine in logLines:
        # проверка строки на memory
        mem_format_line = re.findall(regex_line_mem, logLine)
        if mem_format_line:
            mem_res.append(float(re.findall(r'[\d\.]+', mem_format_line[0])[1]))
        # проверка строки на bricks
        bricks_format_line = re.findall(regex_line_bricks, logLine)
        if bricks_format_line:
            bricks_res = float(re.findall(r'[\d\.]+', bricks_format_line[0])[0])
    return max(mem_res), bricks_res


# Класс хранит тесты для папки
class TestFolder(Navigation, Report):
    report_file = "_report.txt"
    ft_run = "ft_run"
    ft_reference = "ft_reference"

    def __init__(self, startPath):
        Navigation.__init__(self, startPath)
        Report.__init__(self, self.glueAddress(TestFolder.report_file))

    # Метод проверяет наличие папок ft_run и ft_reference
    def checkExistFolders(self):
        test_success = True
        if not TestFolder.ft_run in self.getLocalDirs():
            test_success = False
            self.reportErrorTest_1(TestFolder.ft_run)
        if not TestFolder.ft_reference in self.getLocalDirs():
            test_success = False
            self.reportErrorTest_1(TestFolder.ft_reference)
        return test_success

    # метод ищет недостающие адреса в списке
    @classmethod
    def noneElements(cls, analisingList, sourseList):
        result = []
        for i in sourseList:
            if not i in analisingList:
                result.append(i)
        return result

    # Метод проверяет набор файлов в папках ft_run и ft_reference
    def checkFilesSet(self):
        regexMask = r'\.stdout$'
        test_success = True
        lost_files_ft_run = self.noneElements(self.getFilesAddressInFolder(self.ft_run, regexMask),
                                              self.getFilesAddressInFolder(self.ft_reference, regexMask))
        lost_files_ft_reference = self.noneElements(self.getFilesAddressInFolder(self.ft_reference, regexMask),
                                                    self.getFilesAddressInFolder(self.ft_run, regexMask))
        if lost_files_ft_run:
            test_success = False
            self.reportErrorTest_2_missing(self.ft_run, self.ft_reference, lost_files_ft_run)
        if lost_files_ft_reference:
            test_success = False
            self.reportErrorTest_2_missing(self.ft_run, self.ft_reference, lost_files_ft_reference)
        return test_success

    # Метод проверяет наличие ошибок в файлах каталога ft_run
    def checkFtRun(self):
        test_success = True
        self.passIn(self.ft_run)
        for log_file_path in self.getFilesAddress():
            lineIterator = 0
            solverFind = False
            for log_file_line in self.getStrFile(log_file_path):
                lineIterator += 1
                # Поиск регистронезависимого слова Error в строке
                if re.findall(r'\b[eE][rR]{2}[oO][rR]\b', log_file_line):
                    self.reportErrorTest_3_Error(log_file_path, lineIterator, log_file_line.rstrip())
                    test_success = False
                if re.match(r'Solver finished at', log_file_line):
                    solverFind = True
            if not solverFind:
                self.reportErrorTest_3_miss_solver(log_file_path)
                test_success = False
        self.passUp()
        return test_success

    # Метод сравнивает файлы в папках
    def checkCompFilesInDirs(self):
        test_success = True
        regexMask = r'\.stdout$'
        filesList = self.getFilesAddressInFolder(self.ft_run, regexMask)
        for logFile in filesList:
            log_ft_run_mem_max, log_ft_run_bricks_last = findMaxSetPeak(self.getStrFileInFolder(self.ft_run, logFile))
            log_ft_ref_mem_max, log_ft_ref_bricks_last = findMaxSetPeak(self.getStrFileInFolder(self.ft_reference, logFile))
            if max(log_ft_run_mem_max, log_ft_ref_mem_max) / min(log_ft_run_mem_max, log_ft_ref_mem_max) > 5.0:
                self.reportErrorTest_4_memory_peak(logFile, log_ft_run_mem_max, log_ft_ref_mem_max)
                test_success = False
            brick_max = max(log_ft_run_bricks_last, log_ft_ref_bricks_last)
            brick_min = min(log_ft_run_bricks_last, log_ft_ref_bricks_last)
            if (brick_max - brick_min)/brick_min > 0.1:
                self.reportErrorTest_4_MESH_Bricks(logFile, log_ft_run_bricks_last, log_ft_ref_bricks_last)
                test_success = False
        return test_success