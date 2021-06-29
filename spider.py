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
for i in range(1,3):
	url = ("https://hub.docker.com/search?q=&type=image")
	res = requests.get(url, headers=headers)
	#error handling
	res.raise_for_status()
	cloneurls = []
	#parsing
	soup = BeautifulSoup(res.text, "lxml")
	#sort "a"class, "list-group-item paginated_item"
	giturls = soup.find_all("a", attr={"class":"imageSearchResult styles__searchResult___EBKah styles__clickable___2bfia"})
	test = soup.a
	print(soup.prettify())
	print("!!!")
	"""
	# https://github.com concatenate
	with open("gitcrawling.txt", "a", encoding="utf8") as f:
			for giturl in giturls:
					cloneurl = "https://github.com" + giturl["href"]
					#git("clone", cloneurl)
					f.write(cloneurl)
					f.write("\n")
	"""
	# docker image pull
	with open("dockercrawling.txt", "a", encoding="utf8") as f:
		for giturl in giturls:
			f.write(giturl)
			f.write("\n")

