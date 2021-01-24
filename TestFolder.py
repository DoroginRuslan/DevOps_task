# Файл содержит реализация класса Navigation, предназначенного для запуска тестов в папке
from Navigation import Navigation
from Report import Report


class TestFolder(Navigation, Report):
    report_file = "report.txt"
    ft_run = "ft_run"
    ft_reference = "ft_reference"

    def __init__(self, startPath):
        Navigation.__init__(self, startPath)
        Report.__init__(self, self.glueAddress(TestFolder.report_file))

    def checkExistFolders(self):
        test_success = True
        if not TestFolder.ft_run in self.getLocalDirs():
            self.addToReportFile("")
