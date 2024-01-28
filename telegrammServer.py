import sys


def inner(first,second):
  x=False
  for i in first:
    if i in second:
      x=True
  print(first)
  print(second)
  return x
import telebot
from telebot import  types
import os
import sqlite3 as sq

token='6788345107:AAEiofgJgo1sAf2t9bkzCZuKficAXt_eDp4'
bot=telebot.TeleBot(token)
typeOfDataForMathPlotLib=""
startDate=""
stopDate=""
okr=0
legend=0
@bot.message_handler(commands=['start'])
def start_message(message):
  print("fgdfgdfg")
  markup=types.ReplyKeyboardMarkup()
  gr=types.KeyboardButton("Построение кастомных графиков")
  tbl=types.KeyboardButton("Создание кастомных таблиц")
  qr1=types.KeyboardButton("Постоение сохраненных графиков")
  tbl1=types.KeyboardButton("Построение сохраненых таблиц")
  cre=types.KeyboardButton("Создание кастомных графиков")
  markup.row(gr,tbl)
  markup.row(qr1,tbl1)
  markup.row(cre)
  bot.send_message(message.chat.id,"Hello",reply_markup=markup)

btf={}
btfList=["isHoton","isWenton","isPumpon","isLighton","inTon","outTon","inHon","outHon","WLon","SHon","Lighton"]
xr=0
@bot.message_handler(content_types=['text'])
def fd(message):
  global typeOfDataForMathPlotLib
  global btf
  if message.text == "Построение кастомных графиков":
    markup=types.InlineKeyboardMarkup()

    isH=types.InlineKeyboardButton(text="isHot",callback_data="isHotoff")
    isW = types.InlineKeyboardButton(text="isWent", callback_data="isWentoff")
    isP = types.InlineKeyboardButton(text="isPump", callback_data="isPumpoff")
    isL = types.InlineKeyboardButton(text="isLight", callback_data="isLightoff")

    inT = types.InlineKeyboardButton(text="Температура внутри", callback_data="inToff")
    outT = types.InlineKeyboardButton(text="Температура снаружи", callback_data="outToff")
    inH = types.InlineKeyboardButton(text="Влажность внутри", callback_data="inHoff")
    outH = types.InlineKeyboardButton(text="Влажность снаружи", callback_data="outHoff")

    WL = types.InlineKeyboardButton(text="Уровень воды", callback_data="WLoff")
    SH = types.InlineKeyboardButton(text="Влажность почвы", callback_data="SHoff")
    Light = types.InlineKeyboardButton(text="Уровень освещения", callback_data="Lightoff")

    done = types.InlineKeyboardButton(text='Всё, я выбрал',callback_data="done")

    btf["isHotoff"]=isH
    btf["isWentoff"] =isW
    btf["isPumpoff"] =isP
    btf["isLightoff"] =isL
    btf["inToff"] =inT
    btf["outToff"] =outT
    btf["inHoff"] =inH
    btf["outHoff"] =outH
    btf["WLoff"] =WL
    btf["SHoff"] =SH
    btf["Lightoff"] =Light

    for i in [isH,isW,isP,isL,inT,outT,inH,outH,WL,SH,Light,done]:
      markup.add(i)
    bot.send_message(message.chat.id,"Выберите значения которые будут на графике",reply_markup=markup)
@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
  global typeOfDataForMathPlotLib
#  print(callback.data)
#  print(btf)
  global btf
  global xr
  if "off" in callback.data:
    markup=types.InlineKeyboardMarkup()
    xr+=1
    for i in btf:
      if i == callback.data:
        print(callback.data)
        btf[i]=types.InlineKeyboardButton(text=btf[i].text+"✅",callback_data=callback.data[:callback.data.index("off")]+"on")
        print(callback.data[:callback.data.index("off")] + "on")
      markup.add(btf[i])
    done = types.InlineKeyboardButton(text='Всё, я выбрал', callback_data="done")
    markup.add(done)
    bot.edit_message_text("Построение графиков",callback.message.chat.id,callback.message.message_id,reply_markup=markup)
  elif callback.data=="done" and xr==0:
    print((not inner(btf,btfList)))
    print("------------------------------")
    markup = types.InlineKeyboardMarkup()
    for i in btf:
      markup.add(btf[i])
    done = types.InlineKeyboardButton(text='Всё, я выбрал', callback_data="done")
    markup.add(done)
    bot.send_message(callback.message.chat.id,"Вы не выбрали ни одного пункта")
    bot.send_message(callback.message.chat.id,"Выберите значения которые будут на графике",reply_markup=markup)
  elif callback.data=="done":
    xr=0
    typeOfDataForMathPlotLib=[]
    for i in btf:
      print(btf[i].callback_data)
      if btf[i].callback_data[-2:len(btf[i].callback_data)] == "on":
        typeOfDataForMathPlotLib.append(btf[i].callback_data[:-2])
    print()
    print(typeOfDataForMathPlotLib)
    typeOfDataForMathPlotLib=";".join(typeOfDataForMathPlotLib)
    bot.send_message(callback.message.chat.id,"Введите начало отсчета данных или выберите оди из готовых вариантов")
    bot.register_next_step_handler(callback.message,getStartdateAndSendstopDate)
#    with open("createGrapth\\incomingData.txt","w") as file:
#      file.write(typeOfDataForMathPlotLib)
"""  elif "on" in callback.data:
    print(callback.data)
    markup=types.InlineKeyboardMarkup()
    print(btf)
    for i in btf:
      print(i)
      print(callback.data)
      print()
      if i == callback.data:
        print("h")
        print(callback.data[:callback.data.index("on")]+"off")
        btf[i]=types.InlineKeyboardButton(text=btf[i].text+"fds",callback_data=callback.data[:callback.data.index("on")]+"off")
        print(btf[i].callback_data)
      markup.add(btf[i])"""
def getStartdateAndSendstopDate(message):
  global startDate
  startDate=message.text
  bot.send_message(message.chat.id,"Введите дату окончания подсчета данных")
  bot.register_next_step_handler(message,getStopdateAndSendOkr)
def getStopdateAndSendOkr(message):
  global stopDate
  stopDate=message.text
  print(stopDate)
  bot.send_message(message.chat.id,"Введите размер округления")
  bot.register_next_step_handler(message,getOkrandsendlegend)
def getOkrandsendlegend(message):
  global okr
  okr=message.text
  print(okr)
  bot.send_message(message.chat.id,"Введите пожалуйста располоэение легенды")
  print(typeOfDataForMathPlotLib)
  bot.register_next_step_handler(message,getLegendAndsaveDataFotMathLotLib)

def getLegendAndsaveDataFotMathLotLib(message):
  global legend
  legend=message.text
  print(legend)
  bot.send_message(message.chat.id,"Данные для создания графика успешно сохранены")
  saveDataFotMathLotLib(message)
def saveDataFotMathLotLib(message):
  print(startDate)
  print(stopDate)
  print(okr)
  markup=types.ReplyKeyboardMarkup()
  gr=types.KeyboardButton("Построение кастомных графиков")
  tbl=types.KeyboardButton("Создание кастомных таблиц")
  qr1=types.KeyboardButton("Постоение сохраненных графиков")
  tbl1=types.KeyboardButton("Построение сохраненых таблиц")
  cre=types.KeyboardButton("Создание кастомных графиков")
  markup.row(gr,tbl)
  markup.row(qr1,tbl1)
  markup.row(cre)
  with open("libr/createGrapth/incomingData.txt", "w") as file:
    writeData="#".join([typeOfDataForMathPlotLib,legend,startDate,stopDate,okr])
    print(writeData)
    file.write(writeData)
  os.system("createGrapth.py")
  with open("libr/createGrapth\\outputData.jpg", "rb") as file:
    d=file.read()
  bot.send_photo(message.chat.id,d,reply_markup=markup)
  print("fdgfdgfdgffgd")

def printAndGetSettings():  # Получаем настройки из файла
  global i
  global settings
  with open("readData\\settings.txt") as file:
    for line in file:
      settings[settingsName[i]] = line.split(" ")[1].rstrip("\n")
      i += 1
  for i in settings:
    print(i, settings[i])

def checkLenSettings():  # Проверяем правильность настроек
  if len(settings) != len(settingsName):
    print("Error in settings.txt file")
    print(f"Need {len(settingsName)} elements, but you have {len(settings)} elements in settings.txt")
    print("Program stoped")
    sys.exit()

i=0
settings={}
settingsName=["type","FTP_Dir","DBNAME","ARCHIVEFOLDER","otherFiles","type_Photo","type_Data_Split","date_Split","time_Split","in_File_Split"]

printAndGetSettings()

checkLenSettings()

if not os.path.isdir("readData"):
  os.mkdir("readData")
if not os.path.isdir("libr/createGrapth"):
  os.mkdir("libr/createGrapth")

with sq.connect(f"{settings['DBNAME']}.db") as con:
  cur=con.cursor()
  cur.execute("""CREATE TABLE IF NOT EXISTS usersData (
  name TEXT,
  datas TEXT,
  startDate TEXT,
  stopDate TEXT,
  legend TEXT,
  okr TEXT,
  updated TEXT)
  """)
print("fdgdf")
bot.polling(none_stop=True)