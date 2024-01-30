import telebot
import sqlite3 as sq
import os
import matplotlib.pyplot as plt
import datetime
import random
import shutil
import logging
import sys

class Use:
    def __init__(self):
        self.settings = {}
        self.settingsName = ["type", "FTP_Dir", "DBNAME", "ARCHIVEFOLDER", "otherFiles", "type_Photo", "type_Data_Split","date_Split", "time_Split", "in_File_Split"]
        self.settingsPath=os.path.abspath(__file__).split("\\")[:-2]
        i=0
        self.settingsPath.append("settings.txt")
        self.settingsPath="\\".join(self.settingsPath)
        print(self.settingsPath)
        with open(self.settingsPath) as file:
            for line in file:
                self.settings[self.settingsName[i]] = line.split(" ")[1].rstrip("\n")
                i += 1
        for i in self.settings:
            print(i, self.settings[i])
        if len(self.settings) != len(self.settingsName):
            logging.critical("Error in settings.txt file")
            logging.info(f"Need {len(self.settingsName)} elements, but you have {len(self.settings)} elements in settings.txt")
            logging.critical("Program stoped")
            sys.exit()
        self.db = teplData(self.settings["DBNAME"])

    def checkFolder(self):
        print("AAAAAAAAAAAAAAAAAAAAAAAAA")
        self.files = os.listdir(self.settings["FTP_Dir"])
        print(self.files)
#        self.getOnlyFiles()
        self.comands=[]
        print(self.files)
        for i in self.files:
            print(i)
            x=File(i,self.settings)
            data=x.read()
            print(f"{self.settings['FTP_Dir']}\\{i}")
            print(f"{self.settings['FTP_Dir']}\\{i}")
            print(f"{self.settings['FTP_Dir']}\\{i}")
            print(f"{self.settings['FTP_Dir']}\\{i}")
            print(f"{self.settings['FTP_Dir']}\\{i}")
            x.move()
            self.db.uploadDataToDb(data)


    def getOnlyFiles(self):
        f2=[]
        for i in f2:
            if ".txt" in i or self.settings["type_Photo"] in i:
                f2.append(i)
            elif not "." in i:
                shutil.rmtree(f"{self.settings['FTP_Dir']}\\{i}")
            elif self.settings["otherFiles"] == "delete":
                os.remove(f"{self.settings['FTP_Dir']}\\{i}")
        #        print(f"{settings['FTP_Dir']}\\{i}")
        print(f2)
        self.files=f2




class teplData:
    def __init__(self,pathToDB):
        print("----------------------")
        self.path=pathToDB

        self.fl=""
        self.inData=""
        self.datas=[]
        self.locLegend=0
        self.okr=1

        self.data=[]

        a=os.path.abspath(__file__).split("\\")
        a=a[:-1]
        a.append("createGrapth")
        b=a[:]

        a.append("incomingData.txt")
        b.append("outputData.jpg")
        a="\\".join(a)
        b="\\".join(b)
        self.pathToSettings=a
        self.pathToPicture=b
        print(a,b,sep="\n")
        print()
        print(self.path)
        with sq.connect(self.path+".db") as con:
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

    def uploadDataToDb(self,data):
        commandForExe = f"INSERT INTO tepldata VALUES({','.join(data)})"
        print(commandForExe)
        print("---")
        with sq.connect(self.path+".db") as con:
            cur=con.cursor()
            cur.execute(commandForExe)
    def readIncomingData(self):
        with open(self.pathToSettings) as file:
            self.fl = file.read()
        return self.splitReadedIncomingData()

    def splitReadedIncomingData(self):
        self.inData = self.fl.split("#")[0].replace(";", ",")
        self.datas = self.fl.split("#")[0].split(";")
        self.locLegend = int(self.fl.split("#")[1])
        self.stopDate = self.fl.split("#")[3]
        self.startDate=self.fl.split("#")[2]
        return self.getFetchallFromDB()
    def getFetchallFromDB(self):
        with sq.connect(self.path+'.db') as con:
            cur = con.cursor()
            print(f"SELECT {self.inData},dt FROM tepldata WHERE dt BETWEEN '{self.startDate}' and '{self.stopDate}'")
            x = cur.execute(f"SELECT {self.inData},dt FROM tepldata WHERE dt BETWEEN '{self.startDate}' and '{self.stopDate}'")
            y = x.fetchall()
        print(y)
        self.data=y
        return y
"""
    def rotateD2(self):
        self.data=list((zip(*self.data[::-1])))
        print(*self.data,sep="\n")
        self.okrD2()

    def okrD2(self):
        print(self.okr)
        d3 = []
        for l in range(len(self.data)):
            d3.append([])
            prks = []
            k = 0
            for i in self.data[l]:
                prks.append(i)
                if k == self.okr:
                    d3[l].append(sum(prks) // len(prks))
                    prks = []
                    k = 0
                k += 1
        self.data=d3
        print(*d3,sep="\n")
        self.createGrath()
"""
class Grath:
    def __init__(self,dt):
        a=os.path.abspath(__file__).split("\\")
        a=a[:-1]
        a.append("createGrapth")
        b=a[:]
        c=a[:-2]
        c.append("tepl2.db")

        a.append("incomingData.txt")
        b.append("outputData.jpg")
        a="\\".join(a)
        b="\\".join(b)
        self.pathToSettings=a
        self.pathToPicture=b
        print(a,b,sep="\n")
        print()
        self.fl=None
        self.inData=None
        self.datas=None
        self.locLegend=None
        self.startDate=None
        self.stopDate=None
        self.okr=None
        self.data=dt
        self.ldt=None
        self.maxDate=None
        self.minDate=None
        self.scope=None
        self.DtSt=None
        self.dataGrath=[]
        self.dateGrath=[]



    def readIncomingData(self):
        with open(self.pathToSettings) as file:
            self.fl = file.read()
        self.splitReadedIncomingData()

    def splitReadedIncomingData(self):
        self.inData = self.fl.split("#")[0].replace(";", ",")
        self.datas = self.fl.split("#")[0].split(";")
        self.locLegend = int(self.fl.split("#")[1])
        self.stopDate = self.fl.split("#")[3]

    def rotateD2(self):
        self.data = list((zip(*self.data[::1])))
        print(*self.data, sep="\n")
    def tupleToString(self):
        d3=[]
        for i in self.data:
            d3.append(list(i))
        self.data=d3
        print(d3)

    def strToDt(self):
        for i in range(len(self.data[-1])):
            self.data[-1][i]=datetime.datetime.strptime(str(self.data[-1][i]),"%Y-%m-%d %H-%M-%S")
        print(self.data)
        self.ldt={}
        for i in self.data[-1]:
            self.ldt[i]=i

#    def getMaxMinScopeDate(self):
#        self.minDate=min(self.ldt)
#        self.maxDate=max(self.ldt)
#        self.scope=self.maxDate-self.minDate
    def oneDay(self):
        print("OneDay")
        print()
        print(self.data)
        cnt=1
        for i in range(len(self.data[-1])):
            if 0<self.data[-1][i].minute<=5:
                self.dateGrath.append(self.data[-1][i].strftime("%H"))
            else:
                self.dateGrath.append(" "*cnt)
                cnt+=1
#        print(self.dateGrath)
        self.crGR()
    def threeDays(self):
        print("OneDay")
        print()
        print(self.data)
        cnt=1
        for i in range(len(self.data[-1])):
            if 0<self.data[-1][i].minute<=5 and self.data[-1][i].hour%4==0:
                if self.data[-1][i].hour!=0:
                    self.dateGrath.append(" "*cnt+self.data[-1][i].strftime("%H")+" "*cnt)
                else:
                    self.dateGrath.append(" "*cnt+self.data[-1][i].strftime("%H(%m.%d)")+" "*cnt)
            else:
                self.dateGrath.append(" "*cnt)
                cnt+=1
    def twentyOneDays(self):
        print("OneDay")
        print()
        print(self.data)
        cnt=1
        for i in range(len(self.data[-1])):
            if 0<self.data[-1][i].minute<=5 and self.data[-1][i].hour%12==0:
                if self.data[-1][i].hour!=0:
                    self.dateGrath.append(" "*cnt+self.data[-1][i].strftime("%H")+" "*cnt)
                else:
                    self.dateGrath.append(" "*cnt+self.data[-1][i].strftime("%H(%m.%d)")+" "*cnt)
            else:
                self.dateGrath.append(" "*cnt)
                cnt+=1

    def crGR(self):
        print()
        print()
        print()
        print()
        print()
        print(self.scope)
        print(self.dateGrath)
        print(self.data[0])
        print(len(self.dateGrath))
        print(len(self.data[0]))
        plt.plot(self.dateGrath,self.data[0],label="fg")
        plt.legend(loc=4)
        plt.savefig("hello.jpg")
        plt.show()



class File:
    def __init__(self,path,settings):
        self.path=path
        self.strData=""
        self.listData=[]
        self.settings=settings
    def read(self):
        with open(f"{self.settings['FTP_Dir']}\\{self.path}") as file:
            self.strData=file.read()
            self.listData=self.strData.split(";")
            return self.listData
    def move(self):
        print(self.path)
        shutil.move(f"{self.settings['FTP_Dir']}\\{self.path}", f"{self.settings['ARCHIVEFOLDER']}\\{self.path}")



class GenerateData:
    def __init__(self,start_datetime,count,time):
        x=start_datetime.split(";")
        x=list(map(int,x))
        self.start_datetime=datetime.datetime(year=x[0],month=x[1],day=x[2],hour=x[3],minute=x[4],second=x[5])
        print(self.start_datetime)
        self.count=count
        self.time=datetime.timedelta(minutes=time)
    def generate(self):
        print(str(self.start_datetime))
        for i in range(self.count):
            writeData = f"{i};1;'{self.start_datetime.strftime('%Y-%m-%d %H-%M-%S')}';{self.g01()};{self.g01()};{self.g01()};{self.g01()};{self.gt()};{self.gh()};{self.gt()};{self.gh()};{self.f12()};{self.f12()};{self.f12()}"
            with open(f"C:\\my3\\{self.start_datetime.strftime('%Y-%m-%d %H-%M-%S')}.txt","w") as file:
                file.write(writeData)
            self.start_datetime += self.time

    def g01(self):
        return random.randint(0, 1)

    def f12(self):
        return random.randint(200, 600)

    def gt(self):
        return random.randint(10, 30)

    def gh(self):
        return random.randint(50, 80)

#x=teplData("tepl.db")
#x.create()
#x.uploadDataToDb("2;1;'2008-10-23 10:37:22';1;0;1;0;25;80;23;70;300;200;100".split(";"))
"""abc=teplData("C:\\Users\\Nikita\\PycharmProjects\\teplServer\\tepl2")
ab=abc.readIncomingData()
gr=Grath(ab)
gr.rotateD2()
gr.tupleToString()
gr.strToDt()
gr.crGR()
print(gr.data)
print(ab)
print()
print()
print()
print()
print(gr.data)
print(len(gr.data[0]))
print(len(gr.data[1]))"""
