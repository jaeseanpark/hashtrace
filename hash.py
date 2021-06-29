import os
import hashlib
import mariadb
import sys
from tqdm import tqdm

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

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

mydb.autocommit = False
cur = mydb.cursor()

#bufsize and the device to be read and whatnot
bufsize = 4096
buf = 1024
count = -1
storage = '/dev/vg00/data2'
fd1 = os.open(storage, os.O_RDONLY)
#length for the progress bar
length = os.lseek(fd1, 0, os.SEEK_END) / 4096
os.close(fd1)
#read lines from morethanonehash.txt
duplicates = dict()
with open('/home/jaepark/crawling/morethanonehash.txt', 'r') as f2:
	for line in f2.readlines():
		duplicates[line[:-1]] = {'stdbyte': 0, 'hashcnt': 0} 
printProgressBar(0, length, prefix = 'Progress:', suffix = 'Complete', length = 50)
count = -1 
fd = open(storage,'rb')
#main loop
while True:
	count += 1
	readbytes = fd.read(bufsize)
	if not readbytes:
		break
	sha1hash = hashlib.sha1(readbytes)
	sha1hashed = sha1hash.hexdigest()
	"""
	if sha1hashed in duplicates.keys():
		if duplicates[sha1hashed]['hashcnt'] == 0:
			duplicates[sha1hashed]['stdbyte'] = readbytes
			duplicates[sha1hashed]['hashcnt'] += 1
		elif duplicates[sha1hashed]['hashcnt'] == 1:
			if duplicates[sha1hashed]['stdbyte'] == readbytes:
				count += 1
			elif duplicates[sha1hashed]['stdbyte'] != readbytes:
				print("same hash diffrent value!\n")
				sys.exit(count, sha1hashed)
		elif duplicates[sha1hashed]['hashcnt'] > 1:
			if duplicates[sha1hashed]['stdbyte'] == readbytes:
				count += 1
			else:
				print("same hash different val(2)")
				print(count, sha1hashed)
	else:
	 continue
	"""
	mytuple = (sha1hashed, count)
	add_hash(cur, mytuple)
	printProgressBar(count, length, prefix = 'Progress:', suffix = 'Complete', length = 50)
mydb.commit()
cur.close()
mydb.close()
fd.close()
