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

    def checkExistFolders(self):
        test_success = True
        if not TestFolder.ft_run in self.getLocalDirs():
            test_success = False
            self.addToReportFile(TestFolder.ft_run)
        if not TestFolder.ft_reference in self.getLocalDirs():
            test_success = False
            self.addToReportFile(TestFolder.ft_reference)
        return test_success
