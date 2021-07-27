import os
import docker
import subprocess
from tqdm import tqdm
import sys
import shutil
import tarfile


def mkdir(*args):
  return subprocess.check_call(['mkdir'] + list(args))

def rmdir(*args):
  return subprocess.check_call(['rmdir'] + list(args))






#  with open("dockercrawling.txt", "r", encoding="utf8") as f:
#    images = f.readlines()

#  for image in tqdm(images):
  #  source = "/home/jaepark/dockerunpacked/" + image[:-1] + ".tar"
  #  directory = "/home/jaepark/dockerunpacked/" + image[:-1]
  #  mkdir(directory)
  #  dest = directory + "/" + image[:-1] + ".tar"
  #  shutil.move(source, dest)
  #  os.chdir(directory)
  #  tar = tarfile.open(dest, "r:")
  #  tar.extractall()
  #  os.chdir("..")

#  with open("walkunpack.txt", "w") as f:
#    for dirpath, dirnames, filenames in tqdm(os.walk("/home/jaepark/dockerunpacked", followlinks=False)):
#      for name in filenames:
#        f.write(os.path.join(dirpath, name))
#        f.write("\n")

count = 0
with open("walkunpack.txt", "r") as f:
  for line in tqdm(f.readlines()):
    if "layer.tar" in line:
      #  layerdir = line[:-10]
      #  os.chdir(layerdir)
      #  tar = tarfile.open(line[:-1], "r:")
      #  tar.extractall()
      os.remove(line[:-1])
