class Report(object):
    def __init__(self, report_file_path):
        self.report_file_path = report_file_path

    # Метод создаёт файл отчёта в папке
    def initReportFile(self):
        try:
            open(self.report_file_path, "w").close()
        except Exception:
            ("Ошибка создания файла '", self.report_file_path)

    # Метод добавляет запись в файл отчёта
    def addToReportFile(self, data):
        print(self.report_file_path, "\t", data)
        file_report = open(self.report_file_path, "a")
        try:
            file_report.write(data + "\n")
            file_report.close()
            return True
        except Exception:
            print("Ошибка записи в файл '", self.report_file_path)
            file_report.close()
            return False

    # Выводит в файл отчёта ошибку теста 1
    def reportErrorTest_1(self, errFolder):
        self.addToReportFile("directory missing: " + errFolder)

    # Выводит в файл отчёта ошибку теста 2, часть 1
    def reportErrorTest_2_missing(self, errFolder, pairFolder, noneFiles):
        reportText = "In " + errFolder + " there are missing files present in " + pairFolder + ":"
        trigger_comma = False
        for lostFile in noneFiles:
            if trigger_comma:
                reportText += ","
            reportText += " '" + lostFile + "'"
            trigger_comma = True
        self.addToReportFile(reportText)

    # Выводит в файл отчёта ошибку теста 2, часть 2
    def reportErrorTest_2_extra(self, errFolder, pairFolder, noneFiles):
        reportText = "In " + errFolder + " there are extra files files not present in " + pairFolder + ":"
        trigger_comma = False
        for lostFile in noneFiles:
            if trigger_comma:
                reportText += ","
            reportText += " '" + lostFile + "'"
            trigger_comma = True
        self.addToReportFile(reportText)

    # Выводит в файл отчёта ошибку теста 3 (найдено ключевое слово ERROR)
    def reportErrorTest_3_Error(self, filePath, lineNumber, line):
        self.addToReportFile(filePath + "(" + str(lineNumber) + "): " + line)

    # Выводит в файл отчёта ошибку теста 3 (потеряно 'Solver finished at')
    def reportErrorTest_3_miss_solver(self, filePath):
        self.addToReportFile(filePath + ": missing 'Solver finished at'")
