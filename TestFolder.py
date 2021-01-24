# Файл содержит реализация класса Navigation, предназначенного для запуска тестов в папке
from Navigation import Navigation
from Report import Report


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
        test_success = True
        lost_files_ft_run = self.noneElements(self.getFilesAddressInFolder(self.ft_run), self.getFilesAddressInFolder(self.ft_reference))
        lost_files_ft_reference = self.noneElements(self.getFilesAddressInFolder(self.ft_reference), self.getFilesAddressInFolder(self.ft_run))
        if lost_files_ft_run:
            test_success = False
            self.reportErrorTest_2_missing(self.ft_run, self.ft_reference, lost_files_ft_run)
        if lost_files_ft_reference:
            test_success = False
            self.reportErrorTest_2_missing(self.ft_run, self.ft_reference, lost_files_ft_reference)
        return test_success
