class Report(object):
    def __init__(self, report_file_path):
        self.report_file_path = report_file_path

    # Метод создаёт файл отчёта в папке
    def initReportFile(self):
        try:
            open(self.report_file_path, "w").close()
        except Exception:
            print("Ошибка создания файла '", self.report_file_path)

    # Метод добавляет запись в файл отчёта
    def addToReportFile(self, data):
        print(self.report_file_path, "\t", data)
        file_report = open(self.report_file_path, "a")
        try:
            file_report.write(data)
            file_report.close()
            return True
        except Exception:
            print("Ошибка записи в файл '", self.report_file_path)
            file_report.close()
            return False

#    def addToReportFile(self, data):
#        print(self.report_file_path, "\t", data)

    def reportErrorTest_1(self, errFolder):
        self.addToReportFile("directory missing: " + errFolder + "\n")

    def reportErrorTest_2_missing(self, errFolder, pairFolder, noneFiles):
        reportText = "In " + errFolder + " there are missing files present in " + pairFolder + ":"
        trigger_comma = False
        for lostFile in noneFiles:
            if trigger_comma:
                reportText += ","
            reportText += " '" + lostFile + "'"
            trigger_comma = True
        self.addToReportFile(reportText)

    def reportErrorTest_2_extra(self, errFolder, pairFolder, noneFiles):
        reportText = "In " + errFolder + " there are extra files files not present in " + pairFolder + ":"
        trigger_comma = False
        for lostFile in noneFiles:
            if trigger_comma:
                reportText += ","
            reportText += " '" + lostFile + "'"
            trigger_comma = True
        self.addToReportFile(reportText)
