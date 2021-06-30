import os
from tqdm import tqdm
with open("walkfile-windows10_2.txt", "w")as f:
	for dirpath, dirnames, filenames in tqdm(os.walk("/mnt", followlinks=False)):
		for name in filenames:
			f.write(os.path.join(dirpath, name))
			f.write("\n")
	
