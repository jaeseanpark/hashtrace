from bs4 import BeautifulSoup
import requests
import os
import subprocess
import time

def git(*args):
    return subprocess.check_call(['git'] + list(args))

flag = None

while True:
    with open("gitcrawling.txt", "r", encoding="utf8") as f:
        urls = f.readlines()
    url = urls[0]
    flag = 0
    git("clone", url[:-1])
    flag = 1

    if flag == 1:
        del urls[0]
        with open("gitcrawling.txt", "w+", encoding="utf8") as f:
            for url in urls:
                f.write(url)

