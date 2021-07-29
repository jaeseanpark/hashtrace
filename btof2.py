import re
import subprocess
from tqdm import tqdm


f2 = open("cmd_file2.txt", "w")
f3 = open("btof_tmp.txt", "w")

f2.write("open /dev/mapper/loop8p3\n")
f3.write("Block Inode number\n")

with open("btof1_result.txt", "r") as f:
  for line in tqdm(f.readlines()):
    tmplist = re.findall(r'\d+', line)
    if len(tmplist) == 2:
      f2.write("ncheck " + str(tmplist[1]) + "\n")
      f3.write(str(tmplist[0]) + " " + str(tmplist[1]) + "\n")
    elif "<block not found>" in line:
      f2.write("ncheck 0\n")
      f3.write(line)

f2.close()
f3.close()


subprocess.call(["debugfs", "-f", "cmd_file2.txt"])



