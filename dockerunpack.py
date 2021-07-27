import os
from tqdm import tqdm
import docker
import subprocess




def docker(*args):
	return subprocess.check_call(['docker'] + list(args))


flag = 0
with open("dockercrawling.txt", "r", encoding="utf8") as f:
  urls = f.readlines()
for url in urls:
  if url[:-1] != "elasticsearch" and flag == 0:
    continue
  if url[:-1] == "elasticsearch":
    flag = 1
    continue
  docker("pull", url[:-1])

with open("dockercrawling.txt", "r", encoding="utf8") as f:
  images = f.readlines()
for image in tqdm(images):
  imagorg = image[:-1]
  image = "/home/jaepark/dockerunpacked/" + image[:-1] + ".tar"
  docker("save", "-o", image, imagorg)
