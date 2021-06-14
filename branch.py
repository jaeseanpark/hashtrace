import os
import subprocess

#git("command", options, params and what not)
def git(*args):
    return subprocess.check_call(['git'] + list(args))

branches= []
dirs = list(filter(os.path.isdir, os.listdir()))
dirs.sort()
for directory in dirs:
    os.chdir(directory)
    git("branch")
    os.chdir("..")
