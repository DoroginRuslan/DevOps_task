# С этого файла начинается выполнение программы
#import TestFunctions
from TestFolder import TestFolder

print("Hello DevOps")
#TestFunctions.startTests("D:\\Задача на собеседование\\logs", 1)
testFolder = TestFolder("D:\\Задача на собеседование\\logs\\13-ROTATED_FLOWS\\00010-GCS-u_R_0_IW")
testFolder.initReportFile()
