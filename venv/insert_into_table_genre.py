import mysql.connector

mydb = mysql.connector.connect(
  host="myung.mysql.database.azure.com",
  user="cro000@myung",
  passwd="aud123wptjr!",
  database="tmp"
)



sql = "INSERT INTO deal (roadname,province,city,gun,gu,myun,eop,li,dong,address_first,address_second,aptname,floor,area,deal_year,deal_month,deal_day,construction_year,price) " \
      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
for i in range(1,11):
    mycursor = mydb.cursor()
    val = []

    print('2018_' + str(i) + '.txt')
    with open('2018_' + str(i) + '.txt', encoding="utf8") as f:
        for line in f:
            line = str(line)
            list = line.split(',')
            # print(list)
            address = list[0].split(' ')
            province = None
            city = None
            gun = None
            gu = None
            myun = None
            eop = None
            li = None
            dong = None
            for i in address:
                if i[-1] == "도":
                    province = i
                elif i[-1] == "시":
                    city = i
                elif i[-1] == "군":
                    gun = i
                elif i[-1] == "구":
                    if city != "서울특별시" and city != "인천광역시" and city != "대구광역시" and city != "대전광역시" and city != "광주광역시" and city != "울산광역시" and province != "제주특별자치도" and city != "부산광역시":
                        city = i[0:2] + "시"
                        gu = i[2:]
                    else:
                        gu = i
                elif i[-1] == "면":
                    myun = i
                elif i[-1] == "읍":
                    eop = i
                elif i[-1] == "리":
                    li = i
                elif i[-1] == "동" or i[-1] == "가" or i[-1] == "로":
                    dong = i

            address_first = int(list[1])
            address_second = int(list[2])
            aptname = list[3].replace(":", ",")
            area = float(list[4])
            deal_year = int(list[5][0:4])
            deal_month = int(list[5][4:])
            deal_day = 0
            if list[6] == "1~10":
                deal_day = 1
            else:
                deal_day = 2

            if len(list[7]) == 14 and len(list[8]) <= 2:
                # print(list[7])
                price = int(list[7].strip())
                floor = int(list[8])
                cyear = int(list[9])
                roadname = list[10][:-2]
            else:
                # print(list[7],list[8])
                list[7] = list[7] + list[8]
                list[7] = list[7][1:-1]
                price = int(list[7].strip())
                floor = int(list[9])
                cyear = int(list[10])
                roadname = list[11][:-1]

            # print(roadname,province,city,gun,gu,myun,eop,li,dong,address_first,address_second,aptname,floor,area,deal_year,deal_month,deal_day,cyear,price)
            val.append((roadname, province, city, gun, gu, myun, eop, li, dong, address_first, address_second, aptname,
                        floor, area, deal_year, deal_month, deal_day, cyear, price))

    mycursor.executemany(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record was inserted.")
