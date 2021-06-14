import mysql.connector

mydb = mysql.connector.connect(
		host="127.0.0.1",
		user="jaepark",
		password="sean2090072",
		auth_plugin='mysql_native_password',
		database='mydb1'
)

mycursor = mydb.cursor()

sql = "insert into table1 (hash, blkno) values (%s, %d)"
val = (hash, count)
mycursor.execute("sql, val")
mydb.commit()
print(mycursor.rowcount, "record inserted.")
