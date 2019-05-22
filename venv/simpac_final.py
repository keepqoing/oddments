import datetime
import json
from collections import OrderedDict
import csv
import mysql.connector
import numpy as np
import pandas as pd


def connectDB(sql):
    mydb = mysql.connector.connect(
        host="113.198.137.146",
        port=3306,
        user="simpac",
        passwd="simpac123!@#$",
        database="SIMPAC_METAL",
        charset='utf8'
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return myresult


def get_Tapping_Info_By_DayReport(sDate, eDate):
    sql = """SELECT ProdDate,ProdName, MatName1, MatName2, MatName3, MatName4, MatName5, MatName6, MatName7, MatName8, MatName9, MatName10, 
          N1_TappingSTime,N2_TappingSTime,N3_TappingSTime,N4_TappingSTime,N5_TappingSTime,N1_ProdQty, N2_ProdQty, N3_ProdQty, N4_ProdQty, N5_ProdQty 
          FROM TS_EFN_DAYREPORT WHERE ProdDate >= """ + sDate + " AND ProdDate <= " + eDate

    rsSet = connectDB(sql)

    DRInfo = []
    for rs in rsSet:
        DR = {}
        DR["date"] = rs['ProdDate']
        DR["ProdName"] = rs['ProdName']
        DR["N1_TappingTime"] = rs['N1_TappingSTime']
        DR["N2_TappingTime"] = rs['N2_TappingSTime']
        DR["N3_TappingTime"] = rs['N3_TappingSTime']
        DR["N4_TappingTime"] = rs['N4_TappingSTime']
        DR["N5_TappingTime"] = rs['N5_TappingSTime']
        DR["N1_ProdQty"] = rs['N1_ProdQty']
        DR["N2_ProdQty"] = rs['N2_ProdQty']
        DR["N3_ProdQty"] = rs['N3_ProdQty']
        DR["N4_ProdQty"] = rs['N4_ProdQty']
        DR["N5_ProdQty"] = rs['N5_ProdQty']

        Mat = []
        for i in range(1, 11):
            if rs['MatName' + str(i)] != '':
                Mat.append(rs['MatName' + str(i)])
        DR["Mat"] = Mat
        DRInfo.append(DR)

    for DR in DRInfo:
        for i in range(1, 6):
            if DR["N" + str(i) + "_TappingTime"] != '':
                DR["N" + str(i) + "_TappingTime"] = DR["date"] + " " + DR["N" + str(i) + "_TappingTime"]

    for DR in DRInfo:
        for i in range(1, 5):
            sTime = DR["N" + str(i) + "_TappingTime"]
            eTime = DR["N" + str(i + 1) + "_TappingTime"]

            # N4 time이 N3보다 작을 경우
            if sTime != '' and eTime != '' \
                    and datetime.datetime.strptime(eTime, "%Y%m%d %H:%M") < datetime.datetime.strptime(sTime,
                                                                                                       "%Y%m%d %H:%M"):
                eTime = datetime.datetime.strptime(eTime, "%Y%m%d %H:%M") + datetime.timedelta(days=1)
                eTime = eTime.strftime("%Y%m%d %H:%M")

            DR["N" + str(i) + "_TappingTime"] = sTime
            DR["N" + str(i + 1) + "_TappingTime"] = eTime

    return DRInfo


def getData(DRInfo, sDate, eDate):
    result = []
    for index, DR in enumerate(DRInfo):
        for i in range(1, 6):
            sTime = ''
            eTime = ''
            if DR['N' + str(i) + '_TappingTime'] != "":
                sTime = datetime.datetime.strptime(DR['N' + str(i) + '_TappingTime'], "%Y%m%d %H:%M")

            elif DR['N' + str(i) + '_TappingTime'] == "":
                break


            # nk 는 있고 nk+1이 없으면 다음 날의 N1_TappingTime을 eTime로 저장

            if DR['N' + str(i) + '_TappingTime'] != "" \
                    and i + 1 < 6 \
                    and DR['N' + str(i + 1) + '_TappingTime'] == "" \
                    and index != len(DRInfo) - 1:
                eTime = datetime.datetime.strptime(DRInfo[index + 1]['N1_TappingTime'], "%Y%m%d %H:%M")

            elif DR['N' + str(i) + '_TappingTime'] != "" \
                    and i + 1 < 6 \
                    and DR['N' + str(i + 1) + '_TappingTime'] == "" \
                    and index == len(DRInfo) - 1:
                break

            else:
                if i + 1 < 6:
                    eTime = datetime.datetime.strptime(DR['N' + str(i + 1) + '_TappingTime'], "%Y%m%d %H:%M")
                elif index != len(DRInfo) - 1:
                    eTime = datetime.datetime.strptime(DRInfo[index + 1]['N1_TappingTime'], "%Y%m%d %H:%M")

            totalQty = DR['N' + str(i) + '_ProdQty']

            print("sTime : ", sTime, ", eTime : ", eTime, totalQty)
            get = getOneTapData(sTime, eTime, totalQty)
            print("======================1234")

            for data in get:
                print(get[data], DR['date'])
                get[data]['date'] = DR['date']
                get[data]['sTime'] = sTime
                get[data]['eTime'] = eTime
            result.append(get)

    with open('nodeInfo.csv', 'w', newline='') as after:
        # fieldName = ["old_tapPos", "new_tapPos", "stayTime"]
        fieldName = ['date' , 'sTime', 'eTime', 'tapPos', 'stayTime', 'stayTimeNext', 'stayTimePrev', 'prob', 'probNext', 'probPrev', 'ElePo','ElePoNext','ElePoPrev','Qty', 'QtyNext', 'QtyPrev','UPA', 'UPANext', 'UPAPrev']
        writer = csv.DictWriter(after, fieldnames=fieldName)
        writer.writeheader()

        for ondDay in result:
            print("======================")
            for oneTap in ondDay:
                # oneTap['tapPos'] = index

                ondDay[oneTap]['tapPos'] = oneTap
                print(ondDay[oneTap])
                writer.writerow(ondDay[oneTap])




def getOneTapData(sTime, eTime, totalQty):
    sql = "SELECT DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s') AS dates , TAP_POS as tapPos, ElePower  FROM TS_EFN_GETDATA WHERE DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s')>= STR_TO_DATE('" + str(sTime) + "' ,'%Y-%m-%d %H:%i:%S') AND DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s') < STR_TO_DATE('" + str(eTime) + "' ,'%Y-%m-%d %H:%i:%S')"
    print(sql)
    rsSet = connectDB(sql)

    result = []
    tmp = {}
    for i in range(0, 14):
        tmp[str(i)] = {}
        tmp[str(i)]['stayTime'] = 0
        tmp[str(i)]['stayTimeNext'] = 0
        tmp[str(i)]['stayTimePrev'] = 0
        # tmp[str(i)]['count'] = 0
        # tmp[str(i)]['countNext'] = 0
        # tmp[str(i)]['countPrev'] = 0
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

    print(tmp.keys())

    old_tapPos = 0
    sTime = 0
    eTime = 0
    stayTime = 0
    totalcount = 0
    rownum = 0
    new_Data = dict()
    new_Data_keys = []
    elePowerSum = 0

    for rs in rsSet:
        if rownum == 0:
            rownum = 1
            old_tapPos = rs['tapPos']



        new_tapPos = rs['tapPos']
        if old_tapPos != new_tapPos:
            if old_tapPos-1 == new_tapPos:
                tmp[str(int(old_tapPos))]['stayTimePrev'] += stayTime
                tmp[str(int(old_tapPos))]['ElePoPrev'] += elePowerSum
                stayTime = 0
                elePowerSum = 0
                old_tapPos = new_tapPos
            else:
                tmp[str(int(old_tapPos))]['stayTimeNext'] += stayTime
                tmp[str(int(old_tapPos))]['ElePoNext'] += elePowerSum
                stayTime = 0
                elePowerSum = 0
                old_tapPos = new_tapPos

        tmp[str(int(rs['tapPos']))]['stayTime'] += 1
        tmp[str(int(rs['tapPos']))]['ElePo'] += float(rs['ElePower'])
        stayTime += 1
        elePowerSum = float(rs['ElePower'])
        totalcount += 1

    for new_data in tmp:
        print(new_data)

    for new_data in tmp:
        if new_data != '0' and new_data != '13':
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
            if tmp[new_data]['stayTime'] != 0:
                tmp[new_data]['prob'] = tmp[new_data]['stayTime'] / totalcount
            else:
                tmp[new_data]['prob'] = 0
            if tmp[new_data]['stayTimeNext'] != 0:
                tmp[new_data]['probNext'] = tmp[new_data]['stayTimeNext'] / totalcount
            else:
                tmp[new_data]['probNext'] = 0
            tmp[new_data]['probPrev'] = 0
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
            if tmp[new_data]['stayTime'] != 0:
                tmp[new_data]['prob'] = tmp[new_data]['stayTime'] / totalcount
            else:
                tmp[new_data]['prob'] = 0
            tmp[new_data]['probNext'] = 0
            if tmp[new_data]['stayTimePrev']:
                tmp[new_data]['probPrev'] = tmp[new_data]['stayTimePrev'] / totalcount
            else:
                tmp[new_data]['probPrev'] = 0
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

    for qwer in tmp:
        print(tmp[qwer])
    return tmp


DRInfo = get_Tapping_Info_By_DayReport('20181202', "20181230")
for i in DRInfo:
    print(i)
getData(DRInfo, '20181202', "20181230")



#
# result = []
# for i, dayReport in enumerate(countdict):
#     for onetofive in range(1,5):
#         if dayReport['N' + str(onetofive) + '_TappingTime'] != dayReport['date'] + " "  and dayReport['N' + str(onetofive+1) + '_TappingTime'] == dayReport['date'] + " ":
#             sDate = datetime.datetime.strptime(dayReport['N' + str(onetofive) + '_TappingTime'], "%Y%m%d %H:%M") + datetime.timedelta(days=1)
#             if datetime.datetime.strptime(countdict[i]['date'], "%Y%m%d") - datetime.timedelta(days = -1) < datetime.datetime.strptime(q1eDate, "%Y%m%d"):
#                 eDate = datetime.datetime.strptime(countdict[i+1]['N1_TappingTime'], "%Y%m%d %H:%M")
#             print(sDate, eDate)
#             sql = "SELECT DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s') AS dates , TAP_POS as tapPos, TElePower AS avgTElePower, ElePower AS avgElePower, IntPower AS avgIntPower, 1Ampere_A as ampereA1, 1Ampere_B as ampereB1, 1Ampere_C as ampereC1,  1Voltage_A as voltageA1, 1Voltage_B as voltageB1, 1Voltage_C as voltageC1,  1Voltage_A/1Ampere_A as registanceA, 1Voltage_B/1Ampere_B as registanceB, 1Voltage_C/1Ampere_C as registanceC,  2Ampere_A as ampereA2, 2Ampere_B as ampereB2, 2Ampere_C as ampereC2,  2Voltage_A as voltageA2, 2Voltage_B as voltageB2, 2Voltage_C as voltageC2,  Impedance_A as impedanceA, Impedance_B as impedanceB, Impedance_C as impedanceC, PFPer as pFPer, 3PhasePF_A as pfA, 3PhasePF_B as pfB, 3PhasePF_C as pfC, EPI_A as epiA, EPI_B as epiB, EPI_C as epiC,  TrTemp as trTemp   FROM TS_EFN_GETDATA WHERE DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s') BETWEEN STR_TO_DATE ('" + str(
#                 sDate) + "','%Y%m%d %H:%i:%s') AND STR_TO_DATE ('" + str(eDate) + "','%Y%m%d %H:%i:%s')"
#             print(sql)

# mycursor = mydb.cursor(dictionary=True)
# mycursor.execute(sql)
#
# myresult = mycursor.fetchall()
#
# old_tapPos = 0
# sTime = 0
# eTime = 0
# count = 0
# totalcount = 0
# rownum = 0
# new_Data = dict()
# new_Data_keys = []
# elePowerSum = 0
#
# totalQty = dayReport['N' + str(onetofive) + '_ProdQty']
#
# tmp = {}
# for i in range(0, 14):
#     tmp[str(i)] = OrderedDict()
#     tmp[str(i)]['stayTime'] = 0
#     tmp[str(i)]['stayTimeNext'] = 0
#     tmp[str(i)]['stayTimePrev'] = 0
#     tmp[str(i)]['count'] = 0
#     tmp[str(i)]['countNext'] = 0
#     tmp[str(i)]['countPrev'] = 0
#     tmp[str(i)]['prob'] = 0
#     tmp[str(i)]['probNext'] = 0
#     tmp[str(i)]['probPrev'] = 0
#     tmp[str(i)]['ElePo'] = 0
#     tmp[str(i)]['ElePoNext'] = 0
#     tmp[str(i)]['ElePoPrev'] = 0
#     tmp[str(i)]['Qty'] = 0
#     tmp[str(i)]['QtyNext'] = 0
#     tmp[str(i)]['QtyPrev'] = 0
#     tmp[str(i)]['UPA'] = 0
#     tmp[str(i)]['UPANext'] = 0
#     tmp[str(i)]['UPAPrev'] = 0
#
# print(tmp.keys())
#
# for data in myresult:
#     tmp[str(int(data['tapPos']))]['stayTime'] += 1
#     tmp[str(int(data['tapPos']))]['count'] += 1
#     tmp[str(int(data['tapPos']))]['ElePo'] += float(data['avgElePower'])
#
#     totalcount += 1
#
# for new_data in tmp:
#     if new_data != '0' and new_data != '13':
#         tmp[new_data]['stayTimeNext'] = tmp[str(int(new_data) + 1)]['stayTime']
#         tmp[new_data]['stayTimePrev'] = tmp[str(int(new_data) - 1)]['stayTime']
#         tmp[new_data]['countNext'] = tmp[str(int(new_data) + 1)]['count']
#         tmp[new_data]['countPrev'] = tmp[str(int(new_data) - 1)]['count']
#         if tmp[new_data]['stayTime'] != 0:
#             tmp[new_data]['prob'] = tmp[new_data]['stayTime'] / totalcount
#         else:
#             tmp[new_data]['prob'] = 0
#         if tmp[new_data]['stayTimeNext'] != 0:
#             tmp[new_data]['probNext'] = tmp[new_data]['stayTimeNext'] / totalcount
#         else:
#             tmp[new_data]['probNext'] = 0
#         if tmp[new_data]['stayTimePrev']:
#             tmp[new_data]['probPrev'] = tmp[new_data]['stayTimePrev'] / totalcount
#         else:
#             tmp[new_data]['probPrev'] = 0
#
#         tmp[new_data]['ElePoNext'] = tmp[str(int(new_data) + 1)]['ElePo']
#         tmp[new_data]['ElePoPrev'] = tmp[str(int(new_data) - 1)]['ElePo']
#         tmp[new_data]['Qty'] = tmp[new_data]['prob'] * totalQty
#         tmp[new_data]['QtyNext'] = tmp[new_data]['probNext'] * totalQty
#         tmp[new_data]['QtyPrev'] = tmp[new_data]['probPrev'] * totalQty
#
#         if tmp[new_data]['ElePo'] != 0:
#             tmp[new_data]['UPA'] = tmp[new_data]['ElePo'] / tmp[new_data]['Qty']
#         else:
#             tmp[new_data]['UPA'] = 0
#         if tmp[new_data]['ElePoNext'] != 0:
#             tmp[new_data]['UPANext'] = tmp[new_data]['ElePoNext'] / tmp[new_data]['QtyNext']
#         else:
#             tmp[new_data]['UPANext'] = 0
#         if tmp[new_data]['ElePoPrev'] != 0:
#             tmp[new_data]['UPAPrev'] = tmp[new_data]['ElePoPrev'] / tmp[new_data]['QtyPrev']
#         else:
#             tmp[new_data]['UPAPrev'] = 0
#
#     elif new_data == '0':
#         tmp[new_data]['stayTimeNext'] = tmp[str(int(new_data) + 1)]['stayTime']
#         tmp[new_data]['stayTimePrev'] = 0
#         tmp[new_data]['countNext'] = tmp[str(int(new_data) + 1)]['count']
#         tmp[new_data]['countPrev'] = 0
#         if tmp[new_data]['stayTime'] != 0:
#             tmp[new_data]['prob'] = tmp[new_data]['stayTime'] / totalcount
#         else:
#             tmp[new_data]['prob'] = 0
#         if tmp[new_data]['stayTimeNext'] != 0:
#             tmp[new_data]['probNext'] = tmp[new_data]['stayTimeNext'] / totalcount
#         else:
#             tmp[new_data]['probNext'] = 0
#         tmp[new_data]['probPrev'] = 0
#         tmp[new_data]['ElePoNext'] = tmp[str(int(new_data) + 1)]['ElePo']
#         tmp[new_data]['ElePoPrev'] = 0
#         tmp[new_data]['Qty'] = tmp[new_data]['prob'] * totalQty
#         tmp[new_data]['QtyNext'] = tmp[new_data]['probNext'] * totalQty
#         tmp[new_data]['QtyPrev'] = 0
#
#         if tmp[new_data]['ElePo'] != 0:
#             tmp[new_data]['UPA'] = tmp[new_data]['ElePo'] / tmp[new_data]['Qty']
#         else:
#             tmp[new_data]['UPA'] = 0
#         if tmp[new_data]['ElePoNext'] != 0:
#             tmp[new_data]['UPANext'] = tmp[new_data]['ElePoNext'] / tmp[new_data]['QtyNext']
#         else:
#             tmp[new_data]['UPANext'] = 0
#         tmp[new_data]['UPAPrev'] = 0
#
#
#     elif new_data == '13':
#         tmp[new_data]['stayTimeNext'] = 0
#         tmp[new_data]['stayTimePrev'] = tmp[str(int(new_data) - 1)]['stayTime']
#         tmp[new_data]['countNext'] = 0
#         tmp[new_data]['countPrev'] = tmp[str(int(new_data) - 1)]['count']
#         if tmp[new_data]['stayTime'] != 0:
#             tmp[new_data]['prob'] = tmp[new_data]['stayTime'] / totalcount
#         else:
#             tmp[new_data]['prob'] = 0
#         tmp[new_data]['probNext'] = 0
#         if tmp[new_data]['stayTimePrev']:
#             tmp[new_data]['probPrev'] = tmp[new_data]['stayTimePrev'] / totalcount
#         else:
#             tmp[new_data]['probPrev'] = 0
#         tmp[new_data]['ElePoNext'] = 0
#         tmp[new_data]['ElePoPrev'] = tmp[str(int(new_data) - 1)]['ElePo']
#         tmp[new_data]['Qty'] = tmp[new_data]['prob'] * totalQty
#         tmp[new_data]['QtyNext'] = 0
#         tmp[new_data]['QtyPrev'] = tmp[new_data]['probPrev'] * totalQty
#         if tmp[new_data]['ElePo'] != 0:
#             tmp[new_data]['UPA'] = tmp[new_data]['ElePo'] / tmp[new_data]['Qty']
#         else:
#             tmp[new_data]['UPA'] = 0
#         tmp[new_data]['UPANext'] = 0
#         if tmp[new_data]['ElePoPrev'] != 0:
#             tmp[new_data]['UPAPrev'] = tmp[new_data]['ElePoPrev'] / tmp[new_data]['QtyPrev']
#         else:
#             tmp[new_data]['UPAPrev'] = 0
#
# for qwer in tmp:
#     print(tmp[qwer])
# result.append(tmp)

# elif dayReport['N' + str(onetofive) + '_TappingTime'] != dayReport['date'] + " "  and dayReport['N' + str(onetofive+1) + '_TappingTime'] != dayReport['date'] + " ":
#     sDate = datetime.datetime.strptime(dayReport['N' + str(onetofive) + '_TappingTime'], "%Y%m%d %H:%M")
#     eDate = None
#     if datetime.datetime.strptime(dayReport['N' + str(onetofive) + '_TappingTime'], "%Y%m%d %H:%M") > datetime.datetime.strptime(dayReport['N' + str(onetofive+1) + '_TappingTime'], "%Y%m%d %H:%M"):
#         eDate = datetime.datetime.strptime(dayReport['N' + str(onetofive+1) + '_TappingTime'], "%Y%m%d %H:%M") + datetime.timedelta(days=1)
#     else:
#         eDate = datetime.datetime.strptime(dayReport['N' + str(onetofive+1) + '_TappingTime'], "%Y%m%d %H:%M")
#     print(sDate, eDate)
#
#     sql = "SELECT DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s') AS dates , TAP_POS as tapPos, TElePower AS avgTElePower, ElePower AS avgElePower, IntPower AS avgIntPower, 1Ampere_A as ampereA1, 1Ampere_B as ampereB1, 1Ampere_C as ampereC1,  1Voltage_A as voltageA1, 1Voltage_B as voltageB1, 1Voltage_C as voltageC1,  1Voltage_A/1Ampere_A as registanceA, 1Voltage_B/1Ampere_B as registanceB, 1Voltage_C/1Ampere_C as registanceC,  2Ampere_A as ampereA2, 2Ampere_B as ampereB2, 2Ampere_C as ampereC2,  2Voltage_A as voltageA2, 2Voltage_B as voltageB2, 2Voltage_C as voltageC2,  Impedance_A as impedanceA, Impedance_B as impedanceB, Impedance_C as impedanceC, PFPer as pFPer, 3PhasePF_A as pfA, 3PhasePF_B as pfB, 3PhasePF_C as pfC, EPI_A as epiA, EPI_B as epiB, EPI_C as epiC,  TrTemp as trTemp   FROM TS_EFN_GETDATA WHERE DATE_FORMAT(GetDT, '%Y-%m-%d %H:%i:%s') BETWEEN STR_TO_DATE ('" + str(sDate) + "','%Y%m%d %H:%i:%s') AND STR_TO_DATE ('" + str(eDate) + "','%Y%m%d %H:%i:%s')"
#     print(sql)

#             mycursor = mydb.cursor(dictionary=True)
#             mycursor.execute(sql)
#
#             myresult = mycursor.fetchall()
#
#             old_tapPos = 0
#             sTime = 0
#             eTime = 0
#             count = 0
#             totalcount = 0
#             rownum = 0
#             new_Data = dict()
#             new_Data_keys = []
#             elePowerSum = 0
#
#             totalQty =  dayReport['N' + str(onetofive) + '_ProdQty']
#
#             tmp = {}
#             for i in range(0, 14):
#                 tmp[str(i)] = OrderedDict()
#                 tmp[str(i)]['stayTime'] = 0
#                 tmp[str(i)]['stayTimeNext'] = 0
#                 tmp[str(i)]['stayTimePrev'] = 0
#                 tmp[str(i)]['count'] = 0
#                 tmp[str(i)]['countNext'] = 0
#                 tmp[str(i)]['countPrev'] = 0
#                 tmp[str(i)]['prob'] = 0
#                 tmp[str(i)]['probNext'] = 0
#                 tmp[str(i)]['probPrev'] = 0
#                 tmp[str(i)]['ElePo'] = 0
#                 tmp[str(i)]['ElePoNext'] = 0
#                 tmp[str(i)]['ElePoPrev'] = 0
#                 tmp[str(i)]['Qty'] = 0
#                 tmp[str(i)]['QtyNext'] = 0
#                 tmp[str(i)]['QtyPrev'] = 0
#                 tmp[str(i)]['UPA'] = 0
#                 tmp[str(i)]['UPANext'] = 0
#                 tmp[str(i)]['UPAPrev'] = 0
#
#             print(tmp.keys())
#
#             for data in myresult:
#                 tmp[str(int(data['tapPos']))]['stayTime'] += 1
#                 tmp[str(int(data['tapPos']))]['count'] += 1
#                 tmp[str(int(data['tapPos']))]['ElePo'] += float(data['avgElePower'])
#
#                 totalcount += 1
#
#
#             for new_data in tmp:
#                 if new_data != '0' and new_data != '13':
#                     tmp[new_data]['stayTimeNext'] = tmp[str(int(new_data) + 1)]['stayTime']
#                     tmp[new_data]['stayTimePrev'] = tmp[str(int(new_data) - 1)]['stayTime']
#                     tmp[new_data]['countNext'] = tmp[str(int(new_data) + 1)]['count']
#                     tmp[new_data]['countPrev'] = tmp[str(int(new_data) - 1)]['count']
#                     if tmp[new_data]['stayTime'] != 0:
#                         tmp[new_data]['prob'] = tmp[new_data]['stayTime'] / totalcount
#                     else:
#                         tmp[new_data]['prob'] = 0
#                     if tmp[new_data]['stayTimeNext'] != 0:
#                         tmp[new_data]['probNext'] = tmp[new_data]['stayTimeNext'] / totalcount
#                     else:
#                         tmp[new_data]['probNext'] = 0
#                     if tmp[new_data]['stayTimePrev']:
#                         tmp[new_data]['probPrev'] = tmp[new_data]['stayTimePrev'] / totalcount
#                     else:
#                         tmp[new_data]['probPrev'] = 0
#
#                     tmp[new_data]['ElePoNext'] = tmp[str(int(new_data) + 1)]['ElePo']
#                     tmp[new_data]['ElePoPrev'] = tmp[str(int(new_data) - 1)]['ElePo']
#                     tmp[new_data]['Qty'] = tmp[new_data]['prob'] * totalQty
#                     tmp[new_data]['QtyNext'] = tmp[new_data]['probNext'] * totalQty
#                     tmp[new_data]['QtyPrev'] = tmp[new_data]['probPrev'] * totalQty
#
#                     if tmp[new_data]['ElePo'] != 0:
#                         tmp[new_data]['UPA'] = tmp[new_data]['ElePo'] / tmp[new_data]['Qty']
#                     else:
#                         tmp[new_data]['UPA'] = 0
#                     if tmp[new_data]['ElePoNext'] != 0:
#                         tmp[new_data]['UPANext'] = tmp[new_data]['ElePoNext'] / tmp[new_data]['QtyNext']
#                     else:
#                         tmp[new_data]['UPANext'] = 0
#                     if tmp[new_data]['ElePoPrev'] != 0:
#                         tmp[new_data]['UPAPrev'] = tmp[new_data]['ElePoPrev'] / tmp[new_data]['QtyPrev']
#                     else:
#                         tmp[new_data]['UPAPrev'] = 0
#
#                 elif new_data == '0':
#                     tmp[new_data]['stayTimeNext'] = tmp[str(int(new_data) + 1)]['stayTime']
#                     tmp[new_data]['stayTimePrev'] = 0
#                     tmp[new_data]['countNext'] = tmp[str(int(new_data) + 1)]['count']
#                     tmp[new_data]['countPrev'] = 0
#                     if tmp[new_data]['stayTime'] != 0:
#                         tmp[new_data]['prob'] = tmp[new_data]['stayTime'] / totalcount
#                     else:
#                         tmp[new_data]['prob'] = 0
#                     if tmp[new_data]['stayTimeNext'] != 0:
#                         tmp[new_data]['probNext'] = tmp[new_data]['stayTimeNext'] / totalcount
#                     else:
#                         tmp[new_data]['probNext'] = 0
#                     tmp[new_data]['probPrev'] = 0
#                     tmp[new_data]['ElePoNext'] = tmp[str(int(new_data) + 1)]['ElePo']
#                     tmp[new_data]['ElePoPrev'] = 0
#                     tmp[new_data]['Qty'] = tmp[new_data]['prob'] * totalQty
#                     tmp[new_data]['QtyNext'] = tmp[new_data]['probNext'] * totalQty
#                     tmp[new_data]['QtyPrev'] = 0
#
#                     if tmp[new_data]['ElePo'] != 0:
#                         tmp[new_data]['UPA'] = tmp[new_data]['ElePo'] / tmp[new_data]['Qty']
#                     else:
#                         tmp[new_data]['UPA'] = 0
#                     if tmp[new_data]['ElePoNext'] != 0:
#                         tmp[new_data]['UPANext'] = tmp[new_data]['ElePoNext'] / tmp[new_data]['QtyNext']
#                     else:
#                         tmp[new_data]['UPANext'] = 0
#                     tmp[new_data]['UPAPrev'] = 0
#
#
#                 elif new_data == '13':
#                     tmp[new_data]['stayTimeNext'] = 0
#                     tmp[new_data]['stayTimePrev'] = tmp[str(int(new_data) - 1)]['stayTime']
#                     tmp[new_data]['countNext'] = 0
#                     tmp[new_data]['countPrev'] = tmp[str(int(new_data) - 1)]['count']
#                     if tmp[new_data]['stayTime'] != 0:
#                         tmp[new_data]['prob'] = tmp[new_data]['stayTime'] / totalcount
#                     else:
#                         tmp[new_data]['prob'] = 0
#                     tmp[new_data]['probNext'] = 0
#                     if tmp[new_data]['stayTimePrev']:
#                         tmp[new_data]['probPrev'] = tmp[new_data]['stayTimePrev'] / totalcount
#                     else:
#                         tmp[new_data]['probPrev'] = 0
#                     tmp[new_data]['ElePoNext'] = 0
#                     tmp[new_data]['ElePoPrev'] = tmp[str(int(new_data) - 1)]['ElePo']
#                     tmp[new_data]['Qty'] = tmp[new_data]['prob'] * totalQty
#                     tmp[new_data]['QtyNext'] = 0
#                     tmp[new_data]['QtyPrev'] = tmp[new_data]['probPrev'] * totalQty
#                     if tmp[new_data]['ElePo'] != 0:
#                         tmp[new_data]['UPA'] = tmp[new_data]['ElePo'] / tmp[new_data]['Qty']
#                     else:
#                         tmp[new_data]['UPA'] = 0
#                     tmp[new_data]['UPANext'] = 0
#                     if tmp[new_data]['ElePoPrev'] != 0:
#                         tmp[new_data]['UPAPrev'] = tmp[new_data]['ElePoPrev'] / tmp[new_data]['QtyPrev']
#                     else:
#                         tmp[new_data]['UPAPrev'] = 0
#
#             for qwer in tmp:
#                 print(tmp[qwer])
#             result.append(tmp)
#
# for i in result:
#     print("---------------------------")
#     for j in i:
#         print("    ", j)
#     print("---------------------------")
