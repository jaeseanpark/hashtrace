import os
import hashlib
import mariadb
import sys
from tqdm import tqdm


#add to mariadb
def add_hash(cur, data):
	""" adds hash into database from given data"""
	cur.execute("INSERT INTO table5(hash, blkno) VALUES (?, ?)", data)

#make connection to mariadb
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

#bufsize and the device to be read and whatnot
bufsize = 4096
count = -1
storage = '/dev/vg00/data2'


#read lines from morethanonehash.txt for bit-by-bit comparison
duplicates = dict()
with open('/home/jaepark/crawling/morethanonehash.txt', 'r') as f2:
	for line in f2.readlines():
		duplicates[line[:-1]] = {'stdbyte': 0, 'hashcnt': 0} 



fd = open(storage,'rb')
#main loop
while True:
	count += 1
	readbytes = fd.read(bufsize)
	if not readbytes:
		break
	sha1hash = hashlib.sha1(readbytes)
	sha1hashed = sha1hash.hexdigest()
  #  
  #  for bit-by-bit comparison : 
  #
  #  if sha1hashed in duplicates.keys():
  #    if duplicates[sha1hashed]['hashcnt'] == 0:
  #      duplicates[sha1hashed]['stdbyte'] = readbytes
  #      duplicates[sha1hashed]['hashcnt'] += 1
  #    elif duplicates[sha1hashed]['hashcnt'] == 1:
  #      if duplicates[sha1hashed]['stdbyte'] == readbytes:
  #        count += 1
  #      elif duplicates[sha1hashed]['stdbyte'] != readbytes:
  #        print("same hash diffrent value!\n")
  #        sys.exit(count, sha1hashed)
  #    elif duplicates[sha1hashed]['hashcnt'] > 1:
  #      if duplicates[sha1hashed]['stdbyte'] == readbytes:
  #        count += 1
  #      else:
  #        print("same hash different val(2)")
  #        print(count, sha1hashed)
  #  else:
  #    continue
	mytuple = (sha1hashed, count)
	add_hash(cur, mytuple)
mydb.commit()
cur.close()
mydb.close()
fd.close()
