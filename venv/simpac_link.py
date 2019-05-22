import datetime

import mysql.connector
import numpy as np
import pandas as pd

mydb = mysql.connector.connect(
    host="113.198.137.146",
    port=3306,
    user="simpac",
    passwd="simpac123!@#$",
    database="SIMPAC_METAL",
    charset='utf8'
)
mycursor = mydb.cursor(dictionary=True)

sql = "SELECT * FROM TS_EFN_DAYREPORT WHERE ProdDate > '20181202' AND ProdDate < '20181231'"

mycursor.execute(sql)

myresult = mycursor.fetchall()

countdict = []
for x in myresult:
    print(x)
    Mat = []
    for i in range(1, 11):
        if x["MatName" + str(i)] != '':
            Mat.append(x["MatName" + str(i)])

    print(Mat)
    boil = []
    for i in range(1, 6):
        nBoil = {}
        nBoil["N" + str(i) + "_TappingTime"] = (x['N' + str(i) + "_TappingTime"])
        MatInfo = []
        for i, mati in enumerate(Mat):
            Matj = {}
            Matj["Mati"]


    # for i in range(2, 12):
    #     if x[i] != '':
    #         Mat.append(x[i])

    countdict.append(
        {
            "date": x['ProdDate'],
            "ProdName": x['ProdName'],
            "Mat": Mat,
            "N1_TappingTime": x['N1_TappingTime'],
            "N2_TappingTime": x['N2_TappingTime'],
            "N3_TappingTime": x['N3_TappingTime'],
            "N4_TappingTime": x['N4_TappingTime'],
            "N5_TappingTime": x['N5_TappingTime'],
            "N1_ProdQty": x['N1_ProdQty'],
            "N2_ProdQty": x['N2_ProdQty'],
            "N3_ProdQty": x['N3_ProdQty'],
            "N4_ProdQty": x['N4_ProdQty'],
            "N5_ProdQty": x['N5_ProdQty'],
            "NT_ProdQty": x['NT_ProdQty']
        }
    )
    print(countdict)

sql = "SELECT DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s') AS dates , TAP_POS as tapPos, TElePower AS avgTElePower, ElePower AS avgElePower, IntPower AS avgIntPower  FROM TS_EFN_GETDATA WHERE DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s') BETWEEN STR_TO_DATE ('" + \
      countdict[0]['date'] + " " + countdict[0]['N1_TappingTime'] + ":00','%Y%m%d %H:%i:%s') AND STR_TO_DATE ('" + \
      countdict[0]['date'] + " " + countdict[0]['N2_TappingTime'] + ":00','%Y%m%d %H:%i:%s')"
print(sql)
# sql = "SHOW COLUMNS FROM TS_EFN_GETDATA"

mycursor = mydb.cursor(dictionary=True)
mycursor.execute(sql)

myresult = mycursor.fetchall()

old_tapPos = 0
sTime = 0
eTime = 0
count = 0
rownum = 0
new_Data = dict()
new_Data_keys = []
elePowerSum = 0

for data in myresult:
    if rownum == 0:
        new_Data_keys = data.keys()

        rownum = 1
        sTime = data['dates']
        old_tapPos = data['tapPos']

        for index in new_Data_keys:
            new_Data[index] = []
            new_Data[index].append(data[index])


    else:
        new_tapPos = data['tapPos']
        if (old_tapPos != new_tapPos):

            sTime2 = datetime.datetime(int(sTime[0:4]), int(sTime[5:7]), int(sTime[8:10]), int(sTime[11:13]),
                                       int(sTime[14:16]), int(sTime[17:19]))
            eTime2 = datetime.datetime(int(eTime[0:4]), int(eTime[5:7]), int(eTime[8:10]), int(eTime[11:13]),
                                       int(eTime[14:16]), int(eTime[17:19]))
            stayTime = (eTime2 - sTime2).seconds
            row = {}
            row["old_tapPos"] = old_tapPos
            row["new_tapPos"] = new_tapPos
            row["sTime"] = sTime2.strftime("%Y-%m-%d %H:%M:%S")
            row["eTime"] = eTime2.strftime("%Y-%m-%d %H:%M:%S")
            row["stayTime"] = stayTime

            row["ElePowerSum"] = elePowerSum
            row["ElePowerPerSec"] = elePowerSum / count
            # row["ampereA1"] = np.median(np.array(new_Data['ampereA1']).astype(np.float))
            # row["ampereA1"] = np.median(np.array(new_Data['ampereA1']).astype(np.float))
            # row["ampereB1"] = np.median(np.array(new_Data['ampereB1']).astype(np.float))
            # row["ampereC1"] = np.median(np.array(new_Data['ampereC1']).astype(np.float))
            # row["ampereA2"] = np.median(np.array(new_Data['ampereA2']).astype(np.float))
            # row["ampereB2"] = np.median(np.array(new_Data['ampereB2']).astype(np.float))
            # row["ampereC2"] = np.median(np.array(new_Data['ampereC2']).astype(np.float))
            # row["voltageA1"] = np.median(np.array(new_Data['voltageA1']).astype(np.float))
            # row["voltageB1"] = np.median(np.array(new_Data['voltageB1']).astype(np.float))
            # row["voltageC1"] = np.median(np.array(new_Data['voltageC1']).astype(np.float))
            # row["voltageA2"] = np.median(np.array(new_Data['voltageA2']).astype(np.float))
            # row["voltageB2"] = np.median(np.array(new_Data['voltageB2']).astype(np.float))
            # row["voltageC2"] = np.median(np.array(new_Data['voltageC2']).astype(np.float))
            # row["pfA"] = np.median(np.array(new_Data['pfA']).astype(np.float))
            # row["pfB"] = np.median(np.array(new_Data['pfB']).astype(np.float))
            # row["pfC"] = np.median(np.array(new_Data['pfC']).astype(np.float))
            # row["epiA"] = np.median(np.array(new_Data['epiA']).astype(np.float))
            # row["epiB"] = np.median(np.array(new_Data['epiB']).astype(np.float))
            # row["epiC"] = np.median(np.array(new_Data['epiC']).astype(np.float))
            # row["trTemp"] = np.median(np.array(new_Data['trTemp']).astype(np.float))
            print(row)

            old_tapPos = new_tapPos
            sTime = data['dates']
            eTime = 0
            count = 0
            elePowerSum = 0

        else:
            eTime = data['dates']
            count += 1
            elePowerSum += data['avgElePower']
            for index in new_Data_keys:
                new_Data[index].append(data[index])

print(datetime.datetime(2018, 12, 18, 15, 55, 47, 930))
