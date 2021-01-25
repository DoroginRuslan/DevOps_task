# Файл хранит функции и методы для формирования отчётов

# Функция для рассчёта относительной разницы двух чисел
def calcRelDiff(a, b):
    return (max(a, b) - min(a, b)) / min(a, b)


# Класс хранит методы для формирования отчёта тестов
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

    # Выводит  в файл отчёта ошибку теста 4 (Слишком большая разница между параметрами Memory Working Set Peak)
    def reportErrorTest_4_memory_peak(self, filePath, mp_ft_run, mp_ft_reference):
        self.addToReportFile("{}: different 'Total' of bricks"
                             " (ft_run={}"
                             ", ft_reference={}"
                             ", rel.diff={:.2f}"
                             ", criterion=4)".format(filePath, str(mp_ft_run), str(mp_ft_reference), calcRelDiff(mp_ft_run, mp_ft_reference)))

    # Выводит  в файл отчёта ошибку теста 4 (Слишком большая разница между параметрами MESH::Bricks)
    def reportErrorTest_4_MESH_Bricks(self, filePath, mp_ft_run, mp_ft_reference):
        self.addToReportFile("{}: different 'Total' of bricks"
                             " (ft_run={:g}"
                             ", ft_reference={:g}"
                             ", rel.diff={:.2f}"
                             ", criterion=0.1)".format(filePath, mp_ft_run, mp_ft_reference, calcRelDiff(mp_ft_run, mp_ft_reference)))
