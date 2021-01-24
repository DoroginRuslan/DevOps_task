from TestFolder import TestFolder
import copy


# Возвращает объект класса Navigation с переходом на уровень вниз
def copyNavigationWithIn(testFolder, nextFolder):
#    new_navigation = copy.deepcopy(testFolder)
    new_navigation = TestFolder(testFolder.glueAddress(nextFolder))
    return new_navigation


# Получение списка объектов Navigation с установленными корневыми каталогами тестирования
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


def startTests(rootDir, testsDeep):
    test_dirs = getTestDirs(TestFolder(rootDir), testsDeep)
    for testFolder in test_dirs:
        testFolder.addToReportFile("А? На!\n")
