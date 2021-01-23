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
