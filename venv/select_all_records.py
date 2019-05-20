import mysql.connector

mydb = mysql.connector.connect(
  host="myung.mysql.database.azure.com",
  user="cro000@myung",
  passwd="aud123wptjr!",
  database="tmp"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM deal")

myresult = mycursor.fetchall()

print( len(myresult))
with open('deal.txt', 'w', encoding='utf8') as f2:
  f2.write("도로명,시군구,번지1,번지2,단지명,층,전용면적,계약년도,계약월,계약일,건축년도,거래금액\n")
  for x in myresult:
    # print(x)
    for i in range(1,20):
        if x[i] != None:
            if type(x[i]) == str:
                tmp = str(x[i])

                if i == 12:
                    if tmp.find(",") != -1:
                        # print(tmp)
                        tmp = tmp.replace(',', ":")
                        # print(tmp)

                f2.write(tmp)
            else:
                if i == 17 and x[i] == 1:
                    f2.write("1~10")
                elif i == 17 and x[i] == 2:
                    f2.write("21~30")
                else:
                    f2.write(str(x[i]))
            if i > 1 and i < 8:
                f2.write(" ")
            # elif i == 10:
            #     f2.write("_")
            elif i == 19:
                f2.write("\n")
            else:
                f2.write(",")



    # if(x[17] == 1):
    #   f2.write(x[2]+x[3]+x[4]+x[5]+x[6]+x[7]+x[8]+x[9] + "," + x[10]+"-"+x[11]+","+x[12]+","+x[14]+","+x[15]+x[16]+","+x[19]+",1~10,"+x[13]+","+x[18]+x[0])
    # else:
    #   f2.write(
    #     x[2] + x[3] + x[4] + x[5] + x[6] + x[7] + x[8] + x[9] + "," + x[10] + "-" + x[11] + "," + x[12] + "," + x[
    #       14] + "," + x[15] + x[16] + "," + x[19] + ",21~30," + x[13] + "," + x[18] + x[0])
