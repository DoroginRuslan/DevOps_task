# Файл содержит класс, преданазначенный для навигации по папкам
import os

class Navigation(object):
    # Конструктор, инициирует класс начальным адресом
    def __init__(self, startPath):
        self.flowPath = ""
        if self.setPath(startPath):
            print("Директория '", startPath, "' установлена корневой")
        else:
            print("Путь не является дирректорией")
            exit(-1)

    # Метод устанавливает текущую директорию с проверкой на существование
    def setPath(self, newPath):
        if os.path.isdir(newPath):
            os.chdir(newPath)
            self.flowPath = os.getcwd()
            return True
        else:
            print("Путь не является дирректорией")
            return False

    # Метод выдаёт список папок в директории
    def getLocalDirs(self):
        return [path for path in os.listdir(self.getFlowDir()) if os.path.isdir(path)]

    # Метод выводит текущую директорию
    def getFlowDir(self):
        return self.flowPath

    # Метод обновляет текущую директорию в классе os
    def updateFlowDir(self):
        return self.setPath(self.getFlowDir())

    def passUp(self):
        if self.updateFlowDir():
            return self.setPath("..")
        else:
            print("Не удалось перейти в родительскую директорию")
