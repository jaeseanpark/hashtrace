import os
import subprocess
import time
from tqdm import tqdm

def git(*args):
    return subprocess.check_call(['git'] + list(args))


def main():
    os.chdir('/Volumes/git_trace/')
    print(os.getcwd())
    with open("/Users/mac/hashtrace/gitcrawling2.txt", 'r') as f:
        for line in tqdm(f.readlines()):
            git('clone', line[:-1])

if __name__ == "__main__":
    main()