import os
from tqdm import tqdm
import hashlib
import mariadb



def add_hash(cur, data):
	""" adds hash into database from given data"""
	cur.execute("INSERT INTO table4(hash, file, num) VALUES (?, ?, ?)", data)

try:
	mydb = mariadb.connect(
			host="127.0.0.1",
			user="jaepark",
			password="sean2090072",
			database='mydb1'
	)
except mariadb.Error as e:
	print(f"Error connecting to MariaDB Platform: {e}")
	sys.exit(1)

cur = mydb.cursor()
count = -1

with open("walkfile.txt", "r") as f:
	for line in tqdm(f.readlines()):
		try:
			with open(line[:-1], 'rb') as f2:
				"""
				while True:
					readbytes = f2.read(4096)
					if not readbytes:
						break
					if len(readbytes) < 4096:
						diff = 4096 - len(readbytes)
						readbytes = readbytes + (b"\x00" * diff)
					count += 1
					sha1hash = hashlib.sha1(readbytes)
					sha1hashed = sha1hash.hexdigest()
					mytuple = (sha1hashed, line[:-1], count)
					cur.execute("INSERT INTO table4(hash, file, num) VALUES (?, ?, ?)", mytuple)
					mydb.commit()
				"""
		except IOError as error:
			print(line[:-1])
			continue

cur.close()
mydb.close()
