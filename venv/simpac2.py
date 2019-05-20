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

# for dayReport in countdict:
#     for onetofive in range(1,6):
#         if dayReport['N' + str(onetofive)]


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
totalcount = 0
rownum = 0
new_Data = dict()
new_Data_keys = []
elePowerSum = 0

totalQty = 100.0 #countdict[0]['N1_ProdQty]

tmp = {}
for i in range(0,14):
    tmp[str(i)] = {}
    tmp[str(i)]['stayTime'] = 0
    tmp[str(i)]['stayTimeNext'] = 0
    tmp[str(i)]['stayTimePrev'] = 0
    tmp[str(i)]['count'] = 0
    tmp[str(i)]['countNext'] = 0
    tmp[str(i)]['countPrev'] = 0
    tmp[str(i)]['prob'] = 0
    tmp[str(i)]['probNext'] = 0
    tmp[str(i)]['probPrev'] = 0
    tmp[str(i)]['ElePo'] = 0
    tmp[str(i)]['ElePoNext'] = 0
    tmp[str(i)]['ElePoPrev'] = 0
    tmp[str(i)]['Qty'] = 0
    tmp[str(i)]['QtyNext'] = 0
    tmp[str(i)]['QtyPrev'] = 0
    tmp[str(i)]['UPA'] = 0
    tmp[str(i)]['UPANext'] = 0
    tmp[str(i)]['UPAPrev'] = 0

print(tmp['0'])

for data in myresult:
    print(data['tapPos'])
    print(int(data['tapPos']))
    print(str(int(data['tapPos'])))
    print(tmp[str(int(data['tapPos']))])
    print(tmp[str(int(data['tapPos']))]['stayTime'])
    tmp[str(int(data['tapPos']))]['stayTime'] += 1
    tmp[str(int(data['tapPos']))]['count'] += 1
    tmp[str(int(data['tapPos']))]['ElePo'] += float(data['avgElePower'])

    totalcount += 1

print(tmp)

for new_data in tmp:
    if new_data != '0' and new_data != '13':
        tmp[new_data]['stayTimeNext'] = tmp[str(int(new_data) + 1)]['stayTime']
        tmp[new_data]['stayTimePrev'] = tmp[str(int(new_data) - 1)]['stayTime']
        tmp[new_data]['countNext'] = tmp[str(int(new_data) + 1)]['count']
        tmp[new_data]['countPrev'] = tmp[str(int(new_data) - 1)]['count']
        if tmp[new_data]['stayTime'] != 0:
            tmp[new_data]['prob'] = tmp[new_data]['stayTime'] / totalcount
        else:
            tmp[new_data]['prob'] = 0
        if tmp[new_data]['stayTimeNext'] != 0:
            tmp[new_data]['probNext'] = tmp[new_data]['stayTimeNext'] / totalcount
        else:
            tmp[new_data]['probNext'] = 0
        if tmp[new_data]['stayTimePrev']:
            tmp[new_data]['probPrev'] = tmp[new_data]['stayTimePrev'] / totalcount
        else:
            tmp[new_data]['probPrev'] = 0

        tmp[new_data]['ElePoNext'] = tmp[str(int(new_data) + 1)]['ElePo']
        tmp[new_data]['ElePoPrev'] = tmp[str(int(new_data) - 1)]['ElePo']
        tmp[new_data]['Qty'] = tmp[new_data]['prob'] * totalQty
        tmp[new_data]['QtyNext'] = tmp[new_data]['probNext'] * totalQty
        tmp[new_data]['QtyPrev'] = tmp[new_data]['probPrev'] * totalQty

        if tmp[new_data]['ElePo'] != 0:
            tmp[new_data]['UPA'] = tmp[new_data]['ElePo'] / tmp[new_data]['Qty']
        else:
            tmp[new_data]['UPA'] = 0
        if tmp[new_data]['ElePoNext'] != 0:
            tmp[new_data]['UPANext'] = tmp[new_data]['ElePoNext'] / tmp[new_data]['QtyNext']
        else:
            tmp[new_data]['UPANext'] = 0
        if tmp[new_data]['ElePoPrev'] != 0:
            tmp[new_data]['UPAPrev'] = tmp[new_data]['ElePoPrev'] / tmp[new_data]['QtyPrev']
        else:
            tmp[new_data]['UPAPrev'] = 0

    elif new_data == '0':
        tmp[new_data]['stayTimeNext'] = tmp[str(int(new_data) + 1)]['stayTime']
        tmp[new_data]['stayTimePrev'] = 0
        tmp[new_data]['countNext'] = tmp[str(int(new_data) + 1)]['count']
        tmp[new_data]['countPrev'] = 0
        if tmp[new_data]['stayTime'] != 0:
            tmp[new_data]['prob'] = tmp[new_data]['stayTime'] / totalcount
        else:
            tmp[new_data]['prob'] = 0
        if tmp[new_data]['stayTimeNext'] != 0:
            tmp[new_data]['probNext'] = tmp[new_data]['stayTimeNext'] / totalcount
        else:
            tmp[new_data]['probNext'] = 0
        tmp[new_data]['probPrev'] = 0
        tmp[new_data]['ElePoNext'] = tmp[str(int(new_data) + 1)]['ElePo']
        tmp[new_data]['ElePoPrev'] = 0
        tmp[new_data]['Qty'] = tmp[new_data]['prob'] * totalQty
        tmp[new_data]['QtyNext'] = tmp[new_data]['probNext'] * totalQty
        tmp[new_data]['QtyPrev'] = 0

        if tmp[new_data]['ElePo'] != 0:
            tmp[new_data]['UPA'] = tmp[new_data]['ElePo'] / tmp[new_data]['Qty']
        else:
            tmp[new_data]['UPA'] = 0
        if tmp[new_data]['ElePoNext'] != 0:
            tmp[new_data]['UPANext'] = tmp[new_data]['ElePoNext'] / tmp[new_data]['QtyNext']
        else:
            tmp[new_data]['UPANext'] = 0
        tmp[new_data]['UPAPrev'] = 0


    elif new_data == '13':
        tmp[new_data]['stayTimeNext'] = 0
        tmp[new_data]['stayTimePrev'] = tmp[str(int(new_data) - 1)]['stayTime']
        tmp[new_data]['countNext'] = 0
        tmp[new_data]['countPrev'] = tmp[str(int(new_data) - 1)]['count']
        if tmp[new_data]['stayTime'] != 0:
            tmp[new_data]['prob'] = tmp[new_data]['stayTime'] / totalcount
        else:
            tmp[new_data]['prob'] = 0
        tmp[new_data]['probNext'] = 0
        if tmp[new_data]['stayTimePrev']:
            tmp[new_data]['probPrev'] = tmp[new_data]['stayTimePrev'] / totalcount
        else:
            tmp[new_data]['probPrev'] = 0
        tmp[new_data]['ElePoNext'] = 0
        tmp[new_data]['ElePoPrev'] = tmp[str(int(new_data) - 1)]['ElePo']
        tmp[new_data]['Qty'] = tmp[new_data]['prob'] * totalQty
        tmp[new_data]['QtyNext'] = 0
        tmp[new_data]['QtyPrev'] = tmp[new_data]['probPrev'] * totalQty
        if tmp[new_data]['ElePo'] != 0:
            tmp[new_data]['UPA'] = tmp[new_data]['ElePo'] / tmp[new_data]['Qty']
        else:
            tmp[new_data]['UPA'] = 0
        tmp[new_data]['UPANext'] = 0
        if tmp[new_data]['ElePoPrev'] != 0:
            tmp[new_data]['UPAPrev'] = tmp[new_data]['ElePoPrev'] / tmp[new_data]['QtyPrev']
        else:
            tmp[new_data]['UPAPrev'] = 0

for i in tmp:
    print(tmp[i])
# print(tmp)

# for i, new_data in enumerate(tmp):
#     print("=======",i, new_data)
#     # new_data['stayTimeNext'] = tmp[str(i+1)]['stayTime']
#     # new_data['stayTimePrev'] = tmp[str(i-1)]['stayTime']
#     # new_data['countNext'] = tmp[str(i + 1)]['count']
#     # new_data['countPrev'] = tmp[str(i - 1)]['count']
#     # new_data['prob'] = new_data['stayTime']/totalcount
#     # new_data['probNext'] = new_data['stayTimeNext'] / totalcount
#     # new_data['probPrev'] = new_data['stayTimePrev'] / totalcount
#     # new_data['ElePoNext'] = tmp[str(i + 1)]['ElePo']
#     # new_data['ElePoPrev'] = tmp[str(i - 1)]['ElePo']
#     # new_data['Qty'] = new_data['prob'] * totalQty
#     # new_data['QtyNext'] = new_data['probNext'] * totalQty
#     # new_data['QtyPrev'] = new_data['probPrev'] * totalQty
#     # new_data['UPA'] = new_data['ElePo'] / new_data['Qty']
#     # new_data['UPANext'] = new_data['ElePoNext'] / new_data['QtyNext']
#     # new_data['UPAPrev'] = new_data['ElePoPrev'] / new_data['QtyPrev']
#
# print(tmp)