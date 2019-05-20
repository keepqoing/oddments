import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


with open('address_after3.csv','w',encoding='utf-8-sig', newline='') as after:
    fieldName = ["ocurdt", "ocuryoil", "extingdt", "exintgtm", "ocurgm", "ocurdo", "ocursgg", "ocuremd", "ocurri",
                 "ocurjibun", "address","full_address", "ownersec", "ocurcause",
                 "dmgarea", "dmgmoney", "riskavg", "riskmax", "tempavg", "humidcurr", "humidrel", "humidmin", "windmax",
                 "windavg", "dirmax", "diravg", "raindays", "rainamount"]
    writer = csv.DictWriter(after, fieldnames=fieldName)
    writer.writeheader()

    with open('firedata.csv',encoding='utf-8-sig', newline='') as f1:
        rdr = csv.DictReader(f1)


        for data in rdr:
            flag = 0
            add = set()
            if data["ocurdo"] != ' ':
                add.add(data["ocurdo"])
            if data["ocursgg"] != ' ':
                add.add(data["ocursgg"])
            if data["ocuremd"] != ' ':
                add.add(data["ocuremd"])
            if data["ocurri"] != ' ':
                add.add(data["ocurri"])
            # print(add)

            with open('address_after.csv', encoding='utf-8-sig', newline='') as f2:
                rdr2 = csv.DictReader(f2)

                for data2 in rdr2:
                    add2 = set()
                    if data2["sido"] != '':
                        add2.add(data2["sido"])
                    if data2["sgg"] != '':
                        add2.add(data2["sgg"])
                    if data2["dong1"] != '':
                        add2.add(data2["dong1"])
                    if data2["dong2"] != '':
                        add2.add(data2["dong2"])

                    if(add == add2):
                        flag = 1
                        # print("add2",add, add2, add2 == add)
                        row = {}
                        row["ocurdt"] = data['ocurdt']
                        row["ocuryoil"] = data['ocuryoil']
                        row["extingdt"] = data['extingdt']
                        row["exintgtm"] = data['exintgtm']
                        row["ocurgm"] = data['ocurgm']
                        row["ocurdo"] = data2['sido2']
                        row["ocursgg"] = data2['sgg2']
                        row["ocuremd"] = data2['dong12']
                        row["ocurri"] = data2['dong22']
                        row["ocurjibun"] = data['ocurjibun']
                        row["address"] = data2['address']
                        row["full_address"] = data2['address'] + data['ocurjibun']
                        row["ownersec"] = data['ownersec']
                        row["ocurcause"] = data['ocurcause']
                        row["dmgarea"] = data['dmgarea']
                        row["dmgmoney"] = data['dmgmoney']
                        row["riskavg"] = data['riskavg']
                        row["riskmax"] = data['riskmax']
                        row["tempavg"] = data['tempavg']
                        row["humidcurr"] = data['humidcurr']
                        row["humidrel"] = data['humidrel']
                        row["humidmin"] = data['humidmin']
                        row["windmax"] = data['windmax']
                        row["windavg"] = data['windavg']
                        row["dirmax"] = data['dirmax']
                        row["diravg"] = data['diravg']
                        row["raindays"] = data['raindays']
                        row["rainamount"] = data['rainamount']
                        writer.writerow(row)
                        break

            if(flag == 0):
                row = {}
                row["ocurdt"] = data['ocurdt']
                row["ocuryoil"] = data['ocuryoil']
                row["extingdt"] = data['extingdt']
                row["exintgtm"] = data['exintgtm']
                row["ocurgm"] = data['ocurgm']
                row["ocurdo"] = data['ocurdo']
                row["ocursgg"] = data['ocursgg']
                row["ocuremd"] = data['ocuremd']
                row["ocurri"] = data['ocurri']
                row["ocurjibun"] = data['ocurjibun']
                row["address"] = 'err'
                row["full_address"] = 'err'
                row["ownersec"] = data['ownersec']
                row["ocurcause"] = data['ocurcause']
                row["dmgarea"] = data['dmgarea']
                row["dmgmoney"] = data['dmgmoney']
                row["riskavg"] = data['riskavg']
                row["riskmax"] = data['riskmax']
                row["tempavg"] = data['tempavg']
                row["humidcurr"] = data['humidcurr']
                row["humidrel"] = data['humidrel']
                row["humidmin"] = data['humidmin']
                row["windmax"] = data['windmax']
                row["windavg"] = data['windavg']
                row["dirmax"] = data['dirmax']
                row["diravg"] = data['diravg']
                row["raindays"] = data['raindays']
                row["rainamount"] = data['rainamount']
                writer.writerow(row)
                    



    # with open('address_after.csv',encoding='utf-8-sig', newline='') as f2:
    #     rdr2 = csv.DictReader(f2)
    #
    #     for data in rdr2:
    #         print(data)




