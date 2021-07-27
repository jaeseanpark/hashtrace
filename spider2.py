from bs4 import BeautifulSoup
import requests
import os
import subprocess
import time
import docker



def git(*args):
    return subprocess.check_call(['git'] + list(args))

def docker(*args):
	return subprocess.check_call(['docker'] + list(args))




flag = None

while True:
	with open("dockercrawling.txt", "r", encoding="utf8") as f:
		urls = f.readlines()
	url = urls[0]
	flag = 0
	"""
	docker("pull", url[:-1])
	docker("image","tag", url[:-1], newurl)
	"""
	newurl = url[:-1]  
	docker("image","rm",newurl)
	flag = 1
	if flag == 1:
		del urls[0]
		with open("dockercrawling.txt", "w+", encoding="utf8") as f:
			for url in urls:
				f.write(url)

