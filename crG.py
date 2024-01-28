def printAndGetSettings(): #Получаем настройки из файла
    global i
    global settings
    with open("readData\\settings.txt") as file:
        for line in file:
            settings[settingsName[i]] = line.split(" ")[1].rstrip("\n")
            i += 1
    for i in settings:
        print(i, settings[i])

def createArchiveDir(): #Создаем папку для старых данных для архивации
    if not os.path.isdir(settings["ARCHIVEFOLDER"]):
        os.mkdir(settings["ARCHIVEFOLDER"])
    logging.info(f"Archive dir created in {settings['ARCHIVEFOLDER']}")

def checkLenSettings(): #Проверяем правильность настроек
    if len(settings) != len(settingsName):
        logging.critical("Error in settings.txt file")
        logging.info(f"Need {len(settingsName)} elements, but you have {len(settings)} elements in settings.txt")
        logging.critical("Program stoped")
        sys.exit()

def createBD():# СОздаём базу данных, если её нет
    with sq.connect(f"{settings['DBNAME']}.db") as con:
        cur=con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS tepldata (
        id INTAGER,
        teplId INTAGER,
        dt TEXT,
        isPump INTAGER,
        isLight INTAGER,
        isHot INTAGER,
        isWent INTAGER,
        inH FLOAT,
        inT FLOAT,
        outH FLOAT,
        outT FLOAT,
        WL INTAGER,
        SH INTAGER,
        Light INTAGER)
        """)
    logging.info("DB created/checked sucseful")
def logExceptBD():#Логируем сключения возникающие при создании таблици
    logging.critical("Error when oppening BD")
    logging.critical(e)
    logging.critical("Program stoped")
    sys.exit()

def firstCheckFolder(): #Получаем список правильных файлов из папки ftp
    x=checkFolder()
    logging.info("Get list of files is cuseful")
    logging.info("Files")
    for i in x:
        logging.info(i)
    return x
def checkFolder(): #Проверяем папку
    files=os.listdir(settings["FTP_Dir"])
    files=getOnlyFiles(files)
    return files

def getOnlyFiles(listOfFiles): #Отсеиваем лишние файлы
    files2=[]
    for i in listOfFiles:
        if ".txt" in i or settings["type_Photo"] in i:
            files2.append(i)

        elif not "." in i:
            shutil.rmtree(f"{settings['FTP_Dir']}\\{i}")
        elif settings["otherFiles"]=="delete":
            os.remove(f"{settings['FTP_Dir']}\\{i}")
#        print(f"{settings['FTP_Dir']}\\{i}")
    return files2

def logFirstCheckFolder(e): #Логируем исключения возникающие при получении данных из папки ftp
    logging.critical("You have error in FTP_Dir in settings.txt")
    logging.critical(e)
#    print(e)
    logging.critical("Program stoped")
    sys.exit()


def uploadOneBDData(i):# Генерим команду и подгружаем данные в таблицу
    commandForExe="INSERT INTO tepldata VALUES("
    values = []
    data=readDataFromFile(i)
#    print(data)
#    print("afds")
    for i in data:
        values.append(data[i])
    commandForExe+=",".join(values)+")"
#    print(commandForExe)
    logging.info("Sucseful get command for execute")
    with sq.connect(f"{settings['DBNAME']}.db") as con:
        cur=con.cursor()
        cur.execute(commandForExe)

def logupLoadOneBDData(i): #Обрабатывем исключения возникающие при генерации команды и загрузки данных в таблицу
    logging.critical("Error when upload to BD")
    logging.critical(e)
    logging.critical("Program stopped")
    sys.exit()

def readDataFromFile(file):#Читаем файл
    with open(f"{settings['FTP_Dir']}\\{file}") as f:
        data=f.read()
    data=data.split(settings["in_File_Split"])
#    print(data)
#    print("f")
    return fullMass(data)

def fullMass(listData):#Забиваем словарь данными одного файла
    x={}
    x["id"]=listData[0]
    x["tpid"] = listData[1]
    x["datetime"] = listData[2]


    x["isPump"]=listData[3]
    x["isLed"]=listData[4]
    x["isHot"]=listData[5]
    x["isWent"]=listData[6]

    x["inH"]=listData[7]
    x["inT"]=listData[8]
    x["outH"]=listData[9]
    x["outT"]=listData[10]

    x["WL"]=listData[11]
    x["SH"]=listData[12]
    x["Light"]=listData[13]
    return x
def moveFileToArchive(file):
    shutil.move(f"{settings['FTP_Dir']}\\{file}",f"{settings['ARCHIVEFOLDER']}\\{file}")


import os,pickle,shutil,logging,sys
import sqlite3 as sq
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
logging.info("Program is starting")
settings={}
settingsName=["type","FTP_Dir","DBNAME","ARCHIVEFOLDER","otherFiles","type_Photo","type_Data_Split","date_Split","time_Split","in_File_Split"]
i=0
printAndGetSettings()

checkLenSettings()

logging.info("Program started sucseful")
createArchiveDir()

try:
    createBD()
except Exception as e:
    logExceptBD()

try:
    x=firstCheckFolder()
except Exception as e:
    logFirstCheckFolder(e)

for i in x:
    try:
#        print(i)
        uploadOneBDData(i)
        moveFileToArchive(i)
    except Exception as e:
        logupLoadOneBDData(e)