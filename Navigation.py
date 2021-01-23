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

    # метод устанавливает текущую директорию с проверкой на существование
    def setPath(self, newPath):
        if os.path.isdir(newPath):
            self.flowPath = newPath
            return True
        else:
            print("Путь не является дирректорией")
            return False

    # Метод выводит текущую директорию
    def getFlowDir(self):
        print(self.flowPath)
