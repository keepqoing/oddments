import csv
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

with open('address_after.csv', 'w', encoding='utf-8-sig', newline='') as after:
    # fieldName = ["old_tapPos", "new_tapPos", "stayTime"]
    fieldName = ["sido", "sgg", "dong1", "dong2", "address", "sido2", "sgg2", "dong12", "dong22"]
    writer = csv.DictWriter(after, fieldnames=fieldName)
    writer.writeheader()

    with open('address.csv', encoding='utf-8-sig', newline='') as f:
        rdr = csv.DictReader(f)

        for data in rdr:
            # print(data)
            row = {}

            add = []
            add.append(data["sido"])
            if (data["sgg"] not in add):
                add.append(data["sgg"])
            if (data["dong1"] not in add
                    and data["dong1"][len(data["dong1"]) - 1] != data["dong2"][len(data["dong2"]) - 1]
                    and data["dong2"][len(data["dong2"]) - 1] != "가"
                    and data["dong2"][len(data["dong2"]) - 1] != "로"):
                add.append(data["dong1"])
            if (data["dong2"] not in add):
                add.append(data["dong2"])

            add_result = str()
            for item in add:
                add_result += item + " "

            print(add_result)

            row["sido"] = data["sido2"]
            row["sgg"] = data["sgg2"][0:len(data["sgg2"]) - 1]
            if (data["dong1"][len(data["dong1"]) - 1] != data["dong2"][len(data["dong2"]) - 1]):
                row["dong1"] = data["dong1"][0:len(data["dong1"]) - 1]
            else:
                row["dong1"] = ""
            row["dong2"] = data["dong2"][0:len(data["dong2"]) - 1]
            row["address"] = add_result

#===========================================================
            add2 = []
            add2.append(data["sido"])
            row["sido2"] = data["sido"]
            if (data["sgg"] not in add2):
                add2.append(data["sgg"])
                row["sgg2"] = data["sgg"]
            else:
                row["sgg2"] = ''

            if (data["dong1"] not in add2
                    and data["dong1"][len(data["dong1"]) - 1] != data["dong2"][len(data["dong2"]) - 1]
                    and data["dong2"][len(data["dong2"]) - 1] != "가"
                    and data["dong2"][len(data["dong2"]) - 1] != "로"):
                add2.append(data["dong1"])
                row["dong12"] = data["dong1"]
            else:
                row["dong12"] = ''
            if (data["dong2"] not in add2):
                add2.append(data["dong2"])
                row["dong22"] = data["dong2"]
            else:
                row["dong22"] = ''

            writer.writerow(row)
