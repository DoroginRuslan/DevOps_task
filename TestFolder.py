# Файл содержит реализация класса Navigation, предназначенного для запуска тестов в папке


from Navigation import Navigation


class TestFolder(Navigation):
    reportFile = "report.txt"

    def __init__(self, startPath):
        Navigation.__init__(self, startPath)
        self.initReportFile()

    # Метод создаёт файл отчёта в папке
    def initReportFile(self):
        try:
            open(self.glueAddress(TestFolder.reportFile), "w").close()
        except Exception:
            print("Ошибка создания файла '", self.glueAddress(TestFolder.reportFile))

    # Метод добавляет запись в файл отчёта
    def addToReportFile(self, data):
        file_report = open(self.glueAddress(TestFolder.reportFile), "a")
        try:
            file_report.write(data)
            file_report.close()
            return True
        except Exception:
            print("Ошибка записи в файл '", self.glueAddress(TestFolder.reportFile))
            file_report.close()
            return False


#    def testCheckFolders(self):
