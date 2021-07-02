import os
import hashlib
import mariadb
import sys
from tqdm import tqdm
from printprogress import printProgressBar


#add to mariadb
def add_hash(cur, data):
  """ adds hash into database from given data"""
  cur.executemany("INSERT INTO table1(hash, blkno) VALUES (?, ?)", data)

#make connection to mariadb
try:
  mydb = mariadb.connect(
      host="127.0.0.1",
      user="jaepark",
      password="sean2090072",
      database='mydb2'
  )
except mariadb.Error as e:
  print(f"Error connecting to MariaDB Platform: {e}")
  sys.exit(1)

cur = mydb.cursor()

#bufsize and the device to be read and whatnot
bufsize = 4096
count = -1
storage = '/dev/vg00/data2'
fd_forlen = os.open(storage, os.O_RDONLY)
total = os.lseek(fd_forlen, 0, os.SEEK_END) / 4096

#read lines from morethanonehash.txt for bit-by-bit comparison
#  duplicates = dict()
#  with open('/home/jaepark/crawling/morethanonehash.txt', 'r') as f2:
#    for line in f2.readlines():
#      duplicates[line[:-1]] = {'stdbyte': 0, 'hashcnt': 0}

printProgressBar(0, total, suffix = 'Complete', length = 50)
mydata = []
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
  mydata.append(mytuple)
  printProgressBar(count, total, suffix = 'Complete', length = 50)
  if count % 1000000 == 0 and count != 0:
    #bulk insert into table every 1,000,000 data
    add_hash(cur, mydata)
    mydb.commit
    mydata.clear()

if mydata:
  #insert any remaining data 
  add_hash(cur, mydata)
  mydb.commit()

cur.close()
mydb.close()
fd.close()
