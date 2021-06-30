import os
import subprocess

#git("command", options, params and what not)
def git(*args):
    return subprocess.check_call(['git'] + list(args))

branches= []
dirs = list(filter(os.path.isdir, os.listdir()))
dirs.sort()
print(dirs)
for directory in dirs:
	if directory == ".git":
		continue
	#  os.chdir(directory)
	git("restore", "--staged", directory)
	#  os.chdir("..")'
