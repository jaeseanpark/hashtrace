import os
from tqdm import tqdm
with open("walkdir.txt", "w")as f:
	for dirpath, dirnames, filenames in tqdm(os.walk("/mnt")):
		for name in dirnames:
			f.write(os.path.join(dirpath, name))
			f.write("\n")
	
