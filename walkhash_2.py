import os
from tqdm import tqdm
import hashlib
import mariadb
import sys
from timeout import timeout
import requests


@timeout(3)
def shortopen(path):
  fd = open(path, 'rb')
  return fd

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

fd = open("walkfile_errlog_2.txt", "w")
mydata = []
with open("walkfile-windows10_2.txt", 'r') as f:
  for line in tqdm(f.readlines()):
    #  if "Timeout" in line:
    #    continue
    #  line = "/mnt" + line[10:]
    try:
      f2 = shortopen(line[:-1])
      while True:
        readbytes = f2.read(4096)
        if not readbytes:
          break
        reallen = len(readbytes)
        if reallen < 4096:
          diff = 4096 - reallen 
          readbytes = readbytes + (b'\x00' * diff)
        count += 1
        sha1hash = hashlib.sha1(readbytes)
        sha1hashed = sha1hash.hexdigest()
        mytuple = (sha1hashed, line[4:-1], reallen)
        mydata.append(mytuple)
        if count % 1000000 == 0 and count != 0:
          # every 1,000,000 data, bulk insert into mariadb
          cur.executemany("INSERT INTO table8(hash, file, len) VALUES (?, ?, ?)", mydata)
          mydb.commit()
          mydata.clear()
      f2.close()
    except IOError as error:
      fd.write("IOError on " + line[4:])
      continue
    except Exception as error:
      fd.write("Timeout on " + line[4:])
      continue
# if iteration stops anywhere between millions: insert any remaining data in mydata
if mydata:
  cur.executemany("INSERT INTO table8(hash, file, len) VALUES (?, ?, ?)", mydata)
  mydb.commit()

cur.close()
mydb.close()
fd.close()
