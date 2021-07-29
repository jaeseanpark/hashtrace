import subprocess
from tqdm import tqdm


f2 = open("cmd_file.txt", "w")

f2.write("open /dev/mapper/loop8p3\n")
num = 0
with open("parse_result.txt", "r") as f:
  for line in tqdm(f.readlines()):
    if int(line) < 1054720:
      continue
    num = int(line) / 8
    f2.write("icheck " + str(int(num)) + '\n')

f2.close()

subprocess.call(["debugfs", "-f", "cmd_file.txt"])
