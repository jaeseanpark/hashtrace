import os
from tqdm import tqdm
with open("walkfile-windows10.txt", "w")as f:
	for dirpath, dirnames, filenames in tqdm(os.walk("/mnt")):
		for name in filenames:
			f.write(os.path.join(dirpath, name))
			f.write("\n")
	
