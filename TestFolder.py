# Файл содержит реализация класса Navigation, предназначенного для запуска тестов в папке
from Navigation import Navigation
from Report import Report
import re


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
        self.passIn(self.ft_run)
        for log_file_path in self.getFilesAddress():
            lineIterator = 0
            solverFind = False
            for log_file_line in self.getStrFile(log_file_path):
                lineIterator += 1
                # Поиск регистронезависимого слова Error в строке
                if re.findall(r'\b[eE][rR]{2}[oO][rR]\b', log_file_line):
                    self.reportErrorTest_3_Error(log_file_path, lineIterator, log_file_line.rstrip())
                if re.match(r'Solver finished at', log_file_line):
                    solverFind = True
            if not solverFind:
                self.reportErrorTest_3_miss_solver(log_file_path)
