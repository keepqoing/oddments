import datetime
import mysql.connector
import numpy as np
import csv
# import pandas as pd

mydb = mysql.connector.connect(
    host="113.198.137.146",
    port=3306,
    user="simpac",
    passwd="simpac123!@#$",
    database="SIMPAC_METAL",
    charset='utf8'
)

mycursor = mydb.cursor()

sql = "SELECT ProdDate,ProdName, MatName1, MatName2, MatName3, MatName4, MatName5, MatName6, MatName7, MatName8, MatName9, MatName10,N1_TappingSTime,N2_TappingSTime,N3_TappingSTime,N4_TappingSTime,N5_TappingSTime,N1_ProdQty, N2_ProdQty, N3_ProdQty, N4_ProdQty, N5_ProdQty, NT_ProdQty FROM TS_EFN_DAYREPORT WHERE ProdDate > '20181202' AND ProdDate < '20181231'"

mycursor.execute(sql)

myresult = mycursor.fetchall()

dayReport_list = []
for x in myresult:
    Mat = []
    for i in range(2, 12):
        if x[i] != '':
            Mat.append(x[i])

    dayReport_list.append(
        {
            "date": x[0],
            "ProdName": x[1],
            "Mat": Mat,
            "N1_TappingTime": x[12],
            "N2_TappingTime": x[13],
            "N3_TappingTime": x[14],
            "N4_TappingTime": x[15],
            "N5_TappingTime": x[16],
            "N1_ProdQty": x[17],
            "N2_ProdQty": x[18],
            "N3_ProdQty": x[19],
            "N4_ProdQty": x[20],
            "N5_ProdQty": x[21],
            "NT_ProdQty": x[22]
        }
    )
    print(dayReport_list)



with open('nodeInfo.csv', 'w', newline='') as after:
    # fieldName = ["old_tapPos", "new_tapPos", "stayTime"]
    fieldName = ['old_tapPos', 'new_tapPos', 'sTime', 'eTime', 'stayTime', 'ElePowerSum', 'ElePowerPerSec',
                 'ampereA2_Max', 'ampereB2_Max', 'ampereC2_Max', 'ampereA2_Min', 'ampereB2_Min', 'ampereC2_Min',
                 'ampereA2_Avg', 'ampereB2_Avg', 'ampereC2_Avg',
                 'epiA_Max', 'epiB_Max', 'epiC_Max', 'epiA_Min', 'epiB_Min', 'epiC_Min', 'epiA_Avg', 'epiB_Avg',
                 'epiC_Avg']
    writer = csv.DictWriter(after, fieldnames=fieldName)
    writer.writeheader()

for dayReport in dayReport_list:
    sql = "SELECT DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s') AS dates , TAP_POS as tapPos, TElePower AS avgTElePower, ElePower AS avgElePower, IntPower AS avgIntPower, 1Ampere_A as ampereA1, 2Ampere_A as ampereA2, 2Ampere_B as ampereB2, 2Ampere_C as ampereC2, EPI_A as epiA, EPI_B as epiB, EPI_C as epiC FROM TS_EFN_GETDATA WHERE DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s') BETWEEN STR_TO_DATE ('" + \
          dayReport['date'] + " " + dayReport['N1_TappingTime'] + ":00','%Y%m%d %H:%i:%s') AND STR_TO_DATE ('" + \
          dayReport['date'] + " " + dayReport['N2_TappingTime'] + ":00','%Y%m%d %H:%i:%s')"
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
                row["ampereA2_Max"] = np.max(np.array(new_Data['ampereA2']).astype(np.float))
                row["ampereB2_Max"] = np.max(np.array(new_Data['ampereB2']).astype(np.float))
                row["ampereC2_Max"] = np.max(np.array(new_Data['ampereC2']).astype(np.float))
                row["ampereA2_Min"] = np.min(np.array(new_Data['ampereA2']).astype(np.float))
                row["ampereB2_Min"] = np.min(np.array(new_Data['ampereB2']).astype(np.float))
                row["ampereC2_Min"] = np.min(np.array(new_Data['ampereC2']).astype(np.float))
                row["ampereA2_Avg"] = np.mean(np.array(new_Data['ampereA2']).astype(np.float))
                row["ampereB2_Avg"] = np.mean(np.array(new_Data['ampereB2']).astype(np.float))
                row["ampereC2_Avg"] = np.mean(np.array(new_Data['ampereC2']).astype(np.float))
                row["epiA_Max"] = np.max(np.array(new_Data['epiA']).astype(np.float))
                row["epiB_Max"] = np.max(np.array(new_Data['epiB']).astype(np.float))
                row["epiC_Max"] = np.max(np.array(new_Data['epiC']).astype(np.float))
                row["epiA_Min"] = np.min(np.array(new_Data['epiA']).astype(np.float))
                row["epiB_Min"] = np.min(np.array(new_Data['epiB']).astype(np.float))
                row["epiC_Min"] = np.min(np.array(new_Data['epiC']).astype(np.float))
                row["epiA_Avg"] = np.mean(np.array(new_Data['epiA']).astype(np.float))
                row["epiB_Avg"] = np.mean(np.array(new_Data['epiB']).astype(np.float))
                row["epiC_Avg"] = np.mean(np.array(new_Data['epiC']).astype(np.float))

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