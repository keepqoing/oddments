import mysql.connector

mydb = mysql.connector.connect(
  host="myung.mysql.database.azure.com",
  user="cro000@myung",
  passwd="aud123wptjr!",
  database="tmp"
)

mycursor = mydb.cursor()

sql = "INSERT INTO rating (userID, movieID, rating) VALUES (%s, %s, %s)"
val = []

with open('ratings.dat','rb') as f:
    for line in f:
        line = str(line)
        list = line.split('::')
        list[0] = list[0][2:]
        userID = int(list[0])
        movieID = int(list[1])
        rating = int(list[2])
        val.append((userID, movieID, rating))

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "record was inserted.")
