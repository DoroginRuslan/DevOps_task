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
            result += getTestDirs(copyNavigationWithIn(rootNavigation, localDirs), foldersDeep - 1)
        return result
    else:
        for inFolder in rootNavigation.getLocalDirs():
            result.append(copyNavigationWithIn(rootNavigation, inFolder))
        return result


# Функция последовательно запускает тесты для папки
def runTestsFolder(test_folder):
    test_folder.initFolderReportFile()
    if not test_folder.checkExistFolders():
        return False
    if not test_folder.checkFilesSet():
        return False
    test_result = True
    if not test_folder.checkFtRun():
        test_result = False
    if not test_folder.checkCompFilesInDirs():
        test_result = False
    return test_result


# Функция запускает папки на тестирование
def startTests(rootDir, testsDeep):
    test_dirs = getTestDirs(TestFolder(rootDir), testsDeep)
    for testFolder in test_dirs:
        printTestResult(testFolder, runTestsFolder(testFolder), rootDir)


# Функция выводит в стандартный поток результат тестирования папки
def printTestResult(testFolder, success, rootDir):
    if (success):
        print("OK: " + testFolder.getRelativeAddress(rootDir))
    else:
        print("FAIL: " + testFolder.getRelativeAddress(rootDir))
        print(testFolder.readFolderReportFile().rstrip())