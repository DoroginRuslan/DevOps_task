from Navigation import Navigation
import os
import copy


# Возвращает объект класса Navigation с переходом на уровень вниз
def copyNavigationWithIn(navigation, nextFolder):
    new_navigation = copy.deepcopy(navigation)
    if new_navigation.passIn(nextFolder):
        return new_navigation
    else:
        return None


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
    test_dirs = getTestDirs(Navigation(rootDir), testsDeep)
    return [test.getFlowDir() for test in test_dirs]
