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

with open("dumpe2fs_2.txt", "r") as f:
  for line in tqdm(f.readlines()):
    if "superblock" in line or "bitmap" in line:
      fd1.write(line)
    elif "Inode table" in line or "Reserved GDT" in line:
      fd2.write(line)
    elif "Free blocks:" in line:
      fd3.write(line)
    else:
      print(line)

sys.exit(1)
mylist = []
with open("1.txt", "r") as f:
  for line in tqdm(f.readlines()):
    tmplist = [int(s) for s in re.findall(r'\b\d+\b', line)]
    if "descriptors" in line:
      mylist.extend(list(range(tmplist[1], tmplist[2] + 1)))
    elif "bitmap" in line:
      mylist.append(tmplist[0])
    else:
      print("1" + line)

with open("2.txt", "r") as f:
  for line in tqdm(f.readlines()):
    tmplist = [int(s) for s in re.findall(r'\b\d+\b', line)]
    if len(tmplist) < 2:
      print(line)
      continue
    mylist.extend(list(range(tmplist[0], tmplist[1] + 1)))

freelist = []
with open("3.txt", "r") as f:
  for line in tqdm(f.readlines()):
    tmplist = [int(s) for s in re.findall(r'\b\d+\b', line)]
    if len(tmplist) == 2:
      mylist.extend(list(range(tmplist[0], tmplist[1] + 1)))
      freelist.extend(list(range(tmplist[0], tmplist[1] + 1)))
    elif not tmplist:
      continue
    elif len(tmplist) == 1:
      print(line)
      continue
    elif len(tmplist) > 2:
      print(line)
      i = 0
      if len(tmplist) % 2 == 0:
        while i < len(tmplist):
          mylist.extend(list(range(tmplist[i], tmplist[i+1] + 1)))
          freelist.extend(list(range(tmplist[i], tmplist[i+1] + 1)))
          i += 2
print(len(freelist))
mylist.sort()
print(len(mylist))
mydata = []
count = -1

#  for num in tqdm(mylist):
#    count += 1
#    mytuple = (num,)
#    mydata.append(mytuple)
#    if count % 1000000 == 0 and count != 0:
#      add_hash(cur, mydata)
#      mydb.commit()
#      mydata.clear()
#
#  if mydata:
#    add_hash(cur, mydata)
#    mydb.commit()

cur.close()
mydb.close()
fd1.close()
fd2.close()
fd3.close()

