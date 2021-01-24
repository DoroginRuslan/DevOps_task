# Файл содержит класс, преданазначенный для навигации по папкам
import os


class Navigation(object):
    # Конструктор, инициирует класс начальным адресом
    def __init__(self, startPath):
        self.flowPath = ""
        if self.setPath(startPath):
            print("Директория '", startPath, "' установлена корневой")
        else:
            print("Путь '", startPath, "' не является дирректорией")
            exit(-1)

    # Метод устанавливает текущую директорию с проверкой на существование
    def setPath(self, newPath):
        if os.path.isdir(newPath):
            os.chdir(newPath)
            self.flowPath = os.getcwd()
            return True
        else:
            print("Путь '", newPath, "' не является дирректорией")
            return False

    # Метод выдаёт список папок в директории
    def getLocalDirs(self):
        self.updateFlowDir()
        return [lDir for lDir in os.listdir(self.getFlowDir()) if os.path.isdir(lDir)]

    # Метод выводит текущую директорию
    def getFlowDir(self):
        return self.flowPath

    # Метод обновляет текущую директорию в классе os
    def updateFlowDir(self):
        return self.setPath(self.getFlowDir())

    # Метод для перехода в родительский каталог
    def passUp(self):
        if self.updateFlowDir():
            return self.setPath("..")
        else:
            print("Не удалось перейти в родительскую директорию")
            return False

    # Метод для перехода в дочернюю директорию
    def passIn(self, dirName):
        self.updateFlowDir()
        return self.setPath(dirName)

    # Метод для получения относительных адресов файлов
    def getFilesAddress(self):
        if not self.updateFlowDir():
            return []
        res_address = []
        for folder in os.walk("."):
            for fileFolder in folder[2]:
                res_address.append(
                    os.path.normpath(folder[0] + "/" + fileFolder))
        return res_address

    # Метод для получения данных файла в формате списка строк по относительному пути
    def getStrFile(self, filePath):
        if not self.updateFlowDir():
            return []
        if not os.path.isfile(filePath):
            print("Адрес '", filePath, "' не указывает на файл")
            return []
        try:
            file_data = open(filePath, "r")
            file_text = file_data.readlines()
            file_data.close()
            return file_text
        except Exception:
            print("Ошибка чтения файла '", filePath, "'")
            return []

    # Метод позволяет склеить относительный и текущий адреса
    def glueAddress(self, relative_address):
        return os.path.normpath(self.getFlowDir() + "/" + relative_address)
