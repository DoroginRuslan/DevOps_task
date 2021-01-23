# С этого файла начинается выполнение программы
import Navigation

print("Hello DevOps")
navigation = Navigation.Navigation \
    ('D:\\Задача на собеседование\\logs\\14-HEAT_TRANSFER_IN_SOLID\\00007-NSCV_MG__0_ins_Tfixed_Tfixed')
#    ('D:\\Задача на собеседование\\logs')
print(navigation.getFilesAddress()[1])
for line in navigation.getStrFile(navigation.getFilesAddress()[1]):
    print(line.lstrip().rstrip())
