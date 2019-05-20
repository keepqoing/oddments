import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="movierating"
)

mycursor = mydb.cursor()

sql = "INSERT INTO movies (movieID, title, releaseYear) VALUES (%s, %s, %s)"
val = []

with open('movies.dat','rb') as f:
    for line in f:
        line = str(line)
        list = line.split('::')
        list[0] = list[0][2:]
        list[2] = list[2].replace("\\n'","")
        movieID = int(list[0])
        title = list[1][0:len(list[1])-7]
        releaseYear = int(list[1][len(list[1])-5:len(list[1])-1])
        val.append((movieID, title, releaseYear))

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "record was inserted.")
