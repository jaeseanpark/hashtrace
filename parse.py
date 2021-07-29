import re
import subprocess
import sys
from tqdm import tqdm


f2 = open("parse_result.txt", "w")
f3 = open("parse_original.txt", "w")

with open("ubuntu1.txt", "r") as f:
  for line in tqdm(f.readlines()):
    # if process not VM continue
    if "[AioMgr1-N]" not in line:
      continue
    x = line.split()
    # if not read continue
    if x[6] != 'R':
      continue
    numlist = re.findall(r'\d+', line)
    f2.write(str(numlist[7]) + '\n')
    f3.write(str(numlist[7]) + '+' + str(numlist[8]) + '\n')



