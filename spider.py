from bs4 import BeautifulSoup
import requests
import os
import subprocess

def git(*args):
    return subprocess.check_call(['git'] + list(args))

#user agent string
headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"}

#10page
count = 1
for i in range(1,11):
    url = ("https://gitstar-ranking.com/repositories?page={}" .format(i))
    res = requests.get(url, headers=headers)
    #error handling
    res.raise_for_status()
    cloneurls = []
    #parsing
    soup = BeautifulSoup(res.text, "lxml")
    #sort "a"class, "list-group-item paginated_item"
    giturls = soup.find_all("a", attrs={"class":"list-group-item paginated_item"})

    # https://github.com concatenate
    with open("gitcrawling.txt", "a", encoding="utf8") as f:
        for giturl in giturls:
            cloneurl = "https://github.com" + giturl["href"]
            #git("clone", cloneurl)
            f.write(cloneurl)
            f.write("\n")


