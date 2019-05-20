import datetime
import mysql.connector
import numpy as np
import pandas as pd


def median(v):
    n = len(v)
    sorted_v = sorted(v)  # 정렬해준뒤에
    midpoint = n // 2  # // 로 나누면 int형이 됨. / 로 나누면 float
    if n % 2 == 1:
        return sorted_v[midpoint]  # 리스트가 홀 수면 가운데 값
    else:
        lo = midpoint - 1  # 짝수면 가운데의 2개의 값의 평균
        hi = midpoint
        return (sorted_v[lo] + sorted_v[hi]) / 2


def quantile(x, p):
    p_index = int(p * len(x))
    return sorted(x)[p_index]


def interquartile_range(x):
    return quantile(x, 0.75) - quantile(x, 0.25)


mydb = mysql.connector.connect(
    host="113.198.137.146",
    port=3306,
    user="simpac",
    passwd="simpac123!@#$",
    database="SIMPAC_METAL",
    charset='utf8'
)

mycursor = mydb.cursor()

sql = "SELECT ProdDate,ProdName, MatName1, MatName2, MatName3, MatName4, MatName5, MatName6, MatName7, MatName8, MatName9, MatName10,N1_TappingSTime,N2_TappingSTime,N3_TappingSTime,N4_TappingSTime,N5_TappingSTime,N1_ProdQty, N2_ProdQty, N3_ProdQty, N4_ProdQty, N5_ProdQty FROM TS_EFN_DAYREPORT WHERE ProdDate > '20181217' AND ProdDate < '20181231'"

mycursor.execute(sql)

myresult = mycursor.fetchall()

countdict = []
for x in myresult:
    Mat = []
    for i in range(2, 12):
        if x[i] != '':
            Mat.append(x[i])

    countdict.append(
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
            "N5_ProdQty": x[21]
        }
    )
    print(countdict)

sql = "SELECT DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s') AS dates , TAP_POS as tapPos, TElePower AS avgTElePower, ElePower AS avgElePower, IntPower AS avgIntPower, 1Ampere_A as ampereA1, 1Ampere_B as ampereB1, 1Ampere_C as ampereC1,  1Voltage_A as voltageA1, 1Voltage_B as voltageB1, 1Voltage_C as voltageC1,  1Voltage_A/1Ampere_A as registanceA, 1Voltage_B/1Ampere_B as registanceB, 1Voltage_C/1Ampere_C as registanceC,  2Ampere_A as ampereA2, 2Ampere_B as ampereB2, 2Ampere_C as ampereC2,  2Voltage_A as voltageA2, 2Voltage_B as voltageB2, 2Voltage_C as voltageC2,  Impedance_A as impedanceA, Impedance_B as impedanceB, Impedance_C as impedanceC, PFPer as pFPer, 3PhasePF_A as pfA, 3PhasePF_B as pfB, 3PhasePF_C as pfC, EPI_A as epiA, EPI_B as epiB, EPI_C as epiC,  TrTemp as trTemp   FROM TS_EFN_GETDATA WHERE DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s') BETWEEN STR_TO_DATE ('" + \
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

            sTime2 = datetime.datetime(int(sTime[0:4]), int(sTime[5:7]), int(sTime[8:10]), int(sTime[11:13]), int(sTime[14:16]), int(sTime[17:19]))
            eTime2 = datetime.datetime(int(eTime[0:4]), int(eTime[5:7]), int(eTime[8:10]), int(eTime[11:13]), int(eTime[14:16]), int(eTime[17:19]))
            stayTime = (eTime2 - sTime2).seconds
            row = {}
            row["old_tapPos"] = old_tapPos
            row["new_tapPos"] = new_tapPos
            row["sTime"] = sTime2
            row["eTime"] = eTime2
            row["stayTime"] = stayTime

            row["ElePowerSum"] = elePowerSum
            row["ElePowerPerSec"] = elePowerSum/count
            row["ampereA1"] = np.median(np.array(new_Data['ampereA1']).astype(np.float))
            row["ampereA1"] = np.median(np.array(new_Data['ampereA1']).astype(np.float))
            row["ampereB1"] = np.median(np.array(new_Data['ampereB1']).astype(np.float))
            row["ampereC1"] = np.median(np.array(new_Data['ampereC1']).astype(np.float))
            row["ampereA2"] = np.median(np.array(new_Data['ampereA2']).astype(np.float))
            row["ampereB2"] = np.median(np.array(new_Data['ampereB2']).astype(np.float))
            row["ampereC2"] = np.median(np.array(new_Data['ampereC2']).astype(np.float))
            row["voltageA1"] = np.median(np.array(new_Data['voltageA1']).astype(np.float))
            row["voltageB1"] = np.median(np.array(new_Data['voltageB1']).astype(np.float))
            row["voltageC1"] = np.median(np.array(new_Data['voltageC1']).astype(np.float))
            row["voltageA2"] = np.median(np.array(new_Data['voltageA2']).astype(np.float))
            row["voltageB2"] = np.median(np.array(new_Data['voltageB2']).astype(np.float))
            row["voltageC2"] = np.median(np.array(new_Data['voltageC2']).astype(np.float))
            row["pfA"] = np.median(np.array(new_Data['pfA']).astype(np.float))
            row["pfB"] = np.median(np.array(new_Data['pfB']).astype(np.float))
            row["pfC"] = np.median(np.array(new_Data['pfC']).astype(np.float))
            row["epiA"] = np.median(np.array(new_Data['epiA']).astype(np.float))
            row["epiB"] = np.median(np.array(new_Data['epiB']).astype(np.float))
            row["epiC"] = np.median(np.array(new_Data['epiC']).astype(np.float))
            row["trTemp"] = np.median(np.array(new_Data['trTemp']).astype(np.float))
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