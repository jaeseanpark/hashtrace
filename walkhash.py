import os
from tqdm import tqdm
import hashlib
import mariadb
import sys
from timeout import timeout
import requests


# open with timeout 3seconds
@timeout(3)
def shortopen(path):
	fd = open(path, 'rb')
	return fd

# connect to mariadb
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


#save error logs
#fd = open("walkfile-errlog.txt", "w")

with open("walkfile-errlog.txt", "r") as f:
  for line in tqdm(f.readlines()):
    if "Timeout" in line:
      continue
    line = "/mnt" + line[10:]
		try:
      f2 = shortopen(line[:-1])
      while True:
				readbytes = f2.read(4096)
				if not readbytes:
					break
				if len(readbytes) < 4096:
          # if readbytes < 4KB then pad them with b'\x00' else, different hashes are produced.
					diff = 4096 - len(readbytes)
					readbytes = readbytes + (b"\x00" * diff)
				count += 1
				sha1hash = hashlib.sha1(readbytes)
				sha1hashed = sha1hash.hexdigest()
				mytuple = (sha1hashed, line[4:-1], count)
        # insert into mariaDB
				cur.execute("INSERT INTO table6(hash, file, num) VALUES (?, ?, ?)", mytuple)
        # don't forget to commit
				mydb.commit()
			f2.close()
		except IOError as error:
			#  fd.write("IOError on" + line[4:])
      print(error)
      continue
		except Exception as error:
      # for catching timeout errors
			fd.write("Timeout on" + line[4:])
			print("Timeout on" + line[4:])
			continue

# don't forget to close up
cur.close()
mydb.close()
#  fd.close()

#  print("111")
#  try:
#    f2 = shortopen("/mnt/Users/defaultuser0/AppData/Local/Packages/Microsoft.Windows.CloudExperienceHost_cw5n1h2txyewy/AC/Microsoft/CryptnetUrlCache/Content/57C8EDB95DF3F0AD4EE2DC2B8CFD4157")
#    print("!!!Working on!!!")
#    while True:
#      readbytes = f2.read(4096)
#      if not readbytes:
#        break
#      if len(readbytes) < 4096:
#        diff = 4096 - len(readbytes)
#        readbytes = readbytes + (b"\x00" * diff)
#      count += 1
#      sha1hash = hashlib.sha1(readbytes)
#      sha1hashed = sha1hash.hexdigest()
#      print(sha1hashed)
#    f2.close()
#  except IOError as error:
#    print("IOerror")
#  except Exception as error:
#    print("Timeout")
