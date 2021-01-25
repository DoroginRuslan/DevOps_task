# Файл содержит функции для последовательного запуска тестов и обработки их результатов
from TestFolder import TestFolder


# Возвращает объект класса TestFolder с переходом на уровень вниз
def copyNavigationWithIn(testFolder, nextFolder):
    new_navigation = TestFolder(testFolder.glueAddress(nextFolder))
    return new_navigation


# Получение списка объектов TestFolder с установленными корневыми каталогами тестирования
def getTestDirs(rootNavigation, foldersDeep):
    result = []
    if foldersDeep > 0:
        for localDirs in rootNavigation.getLocalDirs():
            result += getTestDirs(copyNavigationWithIn(rootNavigation, localDirs), foldersDeep-1)
        return result
    else:
        for inFolder in rootNavigation.getLocalDirs():
            result.append(copyNavigationWithIn(rootNavigation, inFolder))
        return result


# Функция запускает тесты
def startTests(rootDir, testsDeep):
    test_dirs = getTestDirs(TestFolder(rootDir), testsDeep)
    for testFolder in test_dirs:
        testFolder.initReportFile()
        if not testFolder.checkExistFolders():
            print(testFolder.getFlowDir() + "\t ошибка в тесте 1, завершение...")
            continue
        if not testFolder.checkFilesSet():
            print(testFolder.getFlowDir() + "\t ошибка в тесте 2, завершение...")
            continue
        testFolder.checkFtRun()
        testFolder.checkCompFilesInDirs()

