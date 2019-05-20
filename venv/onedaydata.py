import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# d = np.random.randn(100)
#
# quant = np.percentile(d, [0, 25, 50, 75, 100])
#
# IQR = np.percentile(d, 75) - np.percentile(d, 25)
#
# lowest = np.percentile(d, 25) - (1.5 * IQR)
# highest = np.percentile(d, 75) + (1.5 * IQR)
#
# print(quant)
# print(np.percentile(d, 75))
# print(np.percentile(d, 25))
# print("IQR", IQR)
# print("median", np.median(d))
# print("lowest", lowest)
# print("highest", highest)
#
# plt.figure()
# plt.boxplot(d)
# plt.grid()
# # plt.hist(da, bins=10, facecolor='red', alpha=0.4, histtype='stepfilled')
# # plt.hist(da, bins=20, facecolor='green', alpha=0.4, histtype='stepfilled')
# plt.show()

#
with open('after5_raw.csv','w', newline='') as after:
    # fieldName = ["old_tapPos", "new_tapPos", "stayTime"]
    fieldName = ["old_tapPos","new_tapPos","sTime","eTime","stayTime","TelePower", "ElePower","ampereA1","ampereB1","ampereC1","ampereA2","ampereB2","ampereC2",
                 "voltageA1","voltageB1","voltageC1","voltageA2","voltageB2","voltageC2","pfA","pfB","pfC","epiA","epiB","epiC","trTemp"]
    writer = csv.DictWriter(after,fieldnames=fieldName)
    writer.writeheader()

    with open('2weeks.csv', newline='') as f:
        rdr = csv.DictReader(f)
        old_tapPos = 0
        sTime = 0
        eTime = 0
        count = 0
        rownum = 0
        tmplist = dict()
        tmpkeys = []

        for data in rdr:
            if (rownum == 0):
                tmp = dict(data)
                tmpkeys = tmp.keys()


                print(tmp.keys())
                rownum = 1
                old_tapPos = data['tapPos']
                sTime = data['dates']

                for index in tmp:
                    tmplist[index] = []
                    tmplist[index].append(data[index])

            else:
                new_tapPos = data['tapPos']
                if (old_tapPos != new_tapPos):

                    sTime2 = datetime(int(sTime[0:4]), int(sTime[4:6]), int(sTime[6:8]), int(sTime[8:10]),
                                      int(sTime[10:12]), int(sTime[12:14]))
                    eTime2 = datetime(int(eTime[0:4]), int(eTime[4:6]), int(eTime[6:8]), int(eTime[8:10]),
                                      int(eTime[10:12]), int(eTime[12:14]))
                    stayTime = (eTime2 - sTime2).seconds
                    row = {}
                    row["old_tapPos"] = old_tapPos
                    row["new_tapPos"] = new_tapPos
                    row["sTime"] = sTime2
                    row["eTime"] = eTime2
                    row["stayTime"] = stayTime
                    row["ElePower"] = np.median(np.array(tmplist['avgElePower']).astype(np.float))
                    row["ampereA1"] = np.median(np.array(tmplist['ampereA1']).astype(np.float))
                    row["ampereA1"] = np.median(np.array(tmplist['ampereA1']).astype(np.float))
                    row["ampereB1"] = np.median(np.array(tmplist['ampereB1']).astype(np.float))
                    row["ampereC1"] = np.median(np.array(tmplist['ampereC1']).astype(np.float))
                    row["ampereA2"] = np.median(np.array(tmplist['ampereA2']).astype(np.float))
                    row["ampereB2"] = np.median(np.array(tmplist['ampereB2']).astype(np.float))
                    row["ampereC2"] = np.median(np.array(tmplist['ampereC2']).astype(np.float))
                    row["voltageA1"] = np.median(np.array(tmplist['voltageA1']).astype(np.float))
                    row["voltageB1"] = np.median(np.array(tmplist['voltageB1']).astype(np.float))
                    row["voltageC1"] = np.median(np.array(tmplist['voltageC1']).astype(np.float))
                    row["voltageA2"] = np.median(np.array(tmplist['voltageA2']).astype(np.float))
                    row["voltageB2"] = np.median(np.array(tmplist['voltageB2']).astype(np.float))
                    row["voltageC2"] = np.median(np.array(tmplist['voltageC2']).astype(np.float))
                    row["pfA"] = np.median(np.array(tmplist['pfA']).astype(np.float))
                    row["pfB"] = np.median(np.array(tmplist['pfB']).astype(np.float))
                    row["pfC"] = np.median(np.array(tmplist['pfC']).astype(np.float))
                    row["epiA"] = np.median(np.array(tmplist['epiA']).astype(np.float))
                    row["epiB"] = np.median(np.array(tmplist['epiB']).astype(np.float))
                    row["epiC"] = np.median(np.array(tmplist['epiC']).astype(np.float))
                    row["trTemp"] = np.median(np.array(tmplist['trTemp']).astype(np.float))
                    writer.writerow(row)


                    for index in tmpkeys:
                        tmplist[index].clear()

                    old_tapPos = new_tapPos
                    sTime = data['dates']
                    eTime = 0
                else:
                    for index in tmpkeys:
                        tmplist[index].append(data[index])
                        eTime = data['dates']






