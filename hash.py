import os
import hashlib
import mysql.connector

mydb = mysql.connector.connect(
		host="127.0.0.1",
		user="jaepark",
		password="sean2090072",
		auth_plugin='mysql_native_password',
		database='mydb1'
)
mycursor = mydb.cursor()

bufsize = 4096
buf = 1024
count = -1
fd = os.open('/dev/dm-0',os.O_RDONLY)

while True:
	count+=1
	readbytes = os.read(fd, buf)
	if not readbytes:
		break
	"""
	sha1hash = hashlib.sha1(readbytes)
	sha1hashed = sha1hash.hexdigest()
	sql = "insert into table1 (hash, blkno) values (%s, %s)"
	val = (sha1hashed, count)
	mycursor.execute(sql, val)
	mydb.commit()
	"""
	if count % 10000 == 0:
		print(count)

print(count)
os.close(fd)
