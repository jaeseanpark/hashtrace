import os
from tqdm import tqdm
import re
import sys
import mariadb
import hashlib


def add_hash(cur, data):
  """ adds hash into database from given data"""
  cur.executemany("INSERT INTO blkno_temp(temp_blkno) VALUES (%s)", data)

#make connection to mariadb
try:
  mydb = mariadb.connect(
      host="127.0.0.1",
      user="jaepark",
      password="sean2090072",
      database='mydb3'
  )
except mariadb.Error as e:
  print(f"Error connecting to MariaDB Platform: {e}")
  sys.exit(1)

cur = mydb.cursor()
fd1 = open("1.txt", "w")
fd2 = open("2.txt", "w")
fd3 = open("3.txt", "w")

with open("dumpe2fs_1.txt", "r") as f:
  for line in tqdm(f.readlines()):
    if "superblock" in line or "bitmap" in line:
      fd1.write(line)
    elif "Inode table" in line:
      fd2.write(line)
    elif "Free blocks:" in line:
      fd3.write(line)
mylist = []
with open("1.txt", "r") as f:
  for line in tqdm(f.readlines()):
    tmplist = [int(s) for s in re.findall(r'\b\d+\b', line)]
    mylist.append(tmplist[0])
    if "descriptors" in line:
      mylist.extend(list(range(tmplist[1], tmplist[2] + 1)))

with open("2.txt", "r") as f:
  for line in tqdm(f.readlines()):
    tmplist = [int(s) for s in re.findall(r'\b\d+\b', line)]
    mylist.extend(list(range(tmplist[0], tmplist[1] + 1)))

with open("3.txt", "r") as f:
  for line in tqdm(f.readlines()):
    tmplist = [int(s) for s in re.findall(r'\b\d+\b', line)]
    if len(tmplist) == 2:
      mylist.extend(list(range(tmplist[0], tmplist[1] + 1)))
    elif not tmplist:
      continue
    elif len(tmplist) == 1:
      print(line)
      continue
    elif len(tmplist) == 4:
      print(str(len(tmplist)) + line)
      mylist.extend(list(range(tmplist[0], tmplist[1] + 1)))
      mylist.extend(list(range(tmplist[2], tmplist[3] + 1)))
    elif len(tmplist) == 8:
      print(str(len(tmplist)) + line)
      mylist.extend(list(range(tmplist[0], tmplist[1] + 1)))
      mylist.extend(list(range(tmplist[2], tmplist[3] + 1)))
      mylist.extend(list(range(tmplist[4], tmplist[5] + 1)))
      mylist.extend(list(range(tmplist[6], tmplist[7] + 1)))
    elif len(tmplist) == 19:
      print(str(len(tmplist)) + line)
      mylist.append(tmplist[0])
      mylist.extend(list(range(tmplist[1], tmplist[2] + 1)))
      mylist.extend(list(range(tmplist[3], tmplist[4] + 1)))
      mylist.extend(list(range(tmplist[5], tmplist[6] + 1)))
      mylist.extend(list(range(tmplist[7], tmplist[8] + 1)))
      mylist.extend(list(range(tmplist[9], tmplist[10] + 1)))
      mylist.extend(list(range(tmplist[11], tmplist[12] + 1)))
      mylist.extend(list(range(tmplist[13], tmplist[14] + 1)))
      mylist.extend(list(range(tmplist[15], tmplist[16] + 1)))
      mylist.extend(list(range(tmplist[17], tmplist[18] + 1)))

mylist.sort()
mydata = []
count = -1
for num in tqdm(mylist):
  count += 1
  mytuple = (num,)
  mydata.append(mytuple)
  if count % 1000000 == 0 and count != 0:
    add_hash(cur, mydata)
    mydb.commit()
    mydata.clear()

if mydata:
  add_hash(cur, mydata)
  mydb.commit()

cur.close()
mydb.close()

