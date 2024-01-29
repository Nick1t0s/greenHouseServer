import sqlite3 as sq
import os
import sys
import matplotlib.pyplot as plt
data=["id","teplId","dt","isPump","isLed","isHot","isWent","inH","inT","outH","outT","WL","SH","Light"]
path=os.path.abspath(__file__).split("\\")[:-1]
path2=os.path.abspath(__file__).split("\\")[:-1]
path.append("tepl.db")
print(path)
path="\\".join(path)

path2.append("createGrapth")
path3=path2[:]
path2.append("incomingData.txt")
path2="\\".join(path2)
path3.append("outputData.jpg")
path3="\\".join(path3)
print(path)
print(path2)
print(path3)
with open(path2) as file:
    fl=file.read()
    inData=fl.split("#")[0].replace(";",",")
    datas=fl.split("#")[0].split(";")
    locLegend=int(fl.split("#")[1])
    okr=int(fl.split("#")[-1])
print(okr)
d2=[]
with sq.connect(path) as con:
    cur=con.cursor()
    print(f"SELECT {inData} FROM tepldata")
    x=cur.execute(f"SELECT {inData} FROM tepldata")
    y=x.fetchall()
    for row in y:
#        print(list(row))
        d2.append(list(row))
"""d21=[[] for i in range(len(row))]
#print(*d21,sep="\n")
for i in range(len(d2)):
    for j in range(len(d2[0])):
        d21[j].append(d2[i][j])"""
print(*d2,sep="\n")
print()
rotated = tuple(zip(*d2[::-1])) # Python 3
print(*rotated,sep="\n")
print(datas)
print(okr)

rotated2=[]
for l in range(len(rotated)):
    rotated2.append([])
    prks=[]
    k=0
    for i in rotated[l]:
        prks.append(i)
        if k == okr:
            rotated2[l].append(sum(prks)//len(prks))
            prks=[]
            k=0
        k+=1
for i in range(len(datas)):
    if datas[i] in ["isHot","isWent","isPump","isLight"]:
        for j in range(len(rotated2[i])):
            x=rotated2[i][j]
            rotated2[i][j]=rotated2[i][j]*max(max(h) for h in rotated2)
print()
print(*rotated,sep="\n")



for i in range(len(rotated2)):
    plt.plot(rotated2[i],label=datas[i])
plt.legend(loc=locLegend)
plt.savefig(f"{path3}")
print(len(rotated[0]))
print(len(rotated2[0]))