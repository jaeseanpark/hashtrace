import os
import subprocess

#git("command", options, params and what not)
def git(*args):
    return subprocess.check_call(['git'] + list(args))

branches= []
with open("branch.txt", "r", encoding="utf8") as f:
    lines = f.readlines()
for branch in lines:
    branch = branch[2:-1]
    branches.append(branch)
print(branches)
dirs = list(filter(os.path.isdir, os.listdir()))
dirs.sort()
i = 0
for directory in dirs:
    os.chdir(directory)
    print(os.getcwd())
    repository = "git@115.145.179.203:root/" + directory + ".git"
    git("push","-u", "--set-upstream", repository, branches[i])
    i += 1
    os.chdir("..")
