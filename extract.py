import os
from tqdm import tqdm
import re
import sys
import mariadb
import hashlib


def add_hash(cur, data):
  """ adds hash into database from given data"""
  cur.executemany("INSERT INTO blkno_temp(temp_blkno) VALUES (%s)", data)

def parserange(x):
  result = []
  for part in x.split(','):
    if '-' in part:
      a, b = part.split('-')
      a, b = int(a), int(b)
      result.extend(range(a, b+1))
    elif part != '':
      a = int(part)
      result.append(a)
  return result

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

with open("dumpe2fs_docker1.txt", "r") as f:
  for line in tqdm(f.readlines()):
    if "superblock" in line or "bitmap" in line:
      fd1.write(line)
    elif "Inode table" in line or "Reserved GDT" in line:
      fd2.write(line)
    elif "Free blocks:" in line:
      fd3.write(line)
fd1.close()
fd2.close()
fd3.close()

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
      continue
    mylist.extend(list(range(tmplist[0], tmplist[1] + 1)))
    
freelist = []
with open("3.txt", "r") as f:
  for line in tqdm(f.readlines()[1:]):
    numlist =  re.split(r'(^[^\d]+)', line[:-1])[2:]
    if numlist[0] == '':
      continue
    tmplist = parserange(numlist[0])
    freelist.extend(tmplist)
    mylist.extend(tmplist)

print("free: " + str(len(freelist)))
mylist.sort()
print("total: " + str(len(mylist)))
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

