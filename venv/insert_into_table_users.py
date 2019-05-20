import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="movierating"
)

mycursor = mydb.cursor()

sql = "INSERT INTO users (userID, gender, age, occupation) VALUES (%s, %s, %s, %s)"
val = []

with open('users.dat','rb') as f:
    for line in f:
        line = str(line)
        list = line.split('::')
        list[0] = list[0][2:]
        list[4] = list[4].replace("\\n'","")
        userID = int(list[0])
        gender = list[1]
        age = int(list[2])
        occupation = int(list[3])
        val.append((userID, gender, age, occupation))

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "record was inserted.")
