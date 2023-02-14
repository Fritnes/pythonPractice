#Libraries
import yaml
import os
import re
import time

def Curuntine_directory():
#Create Curuntine_directory if not exist
    if config["Curuntine_directory"]:
        CHECK_FOLDER = os.path.isdir(config["Curuntine_directory"])
        if not CHECK_FOLDER:
            os.makedirs(config["Curuntine_directory"])

    N = float(config["Day_clear"])
    os.chdir(os.path.join(os.getcwd(), config["Curuntine_directory"]))
    list_of_files = os.listdir()
    current_time = time.time()
    day = 86400
    for i in list_of_files:
        file_location = os.path.join(os.getcwd(), i)
        file_time = os.stat(file_location).st_mtime
        if(file_time < current_time - day*N):
            print(f" Delete : {i}")
            os.remove(file_location)

#Command
def ls(dir, file_patern):
  for x in os.listdir(dir):
    if re.search(file_patern, x):
        print (x)

def mv(dir, file_patern):
  for x in os.listdir(dir):
    if re.search(file_patern, x):
        os.rename(str(dir) + "/" + str(x), str(config["Curuntine_directory"]) + "/" + str(x))

def rm(dir, file_patern):
  for x in os.listdir(dir):
    if re.search(file_patern, x):
        os.remove(str(dir) + "/" + str(x))

def sort(dir, file_patern, sort_path):
  if sort_path:
    CHECK_FOLDER = os.path.isdir(sort_path)
    if not CHECK_FOLDER:
        os.makedirs(sort_path)
  for x in os.listdir(dir):
    if re.search(file_patern, x):
        os.rename(str(dir) + "/" + str(x), str(sort_path) + "/" + str(x))

def do_list(dir, file_patern, command, sort_path=""):
  match command:
    case "ls":
       ls(dir, file_patern)
    case "mv":
       mv(dir, file_patern)
    case "rm":
       rm(dir, file_patern)
    case "sort":
       sort(dir, file_patern, sort_path)

#Load config file
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

Curuntine_directory()
for k, v in config["Directory"].items():
    if "paths" in config["Directory"][k]:
        for path in config["Directory"][k]["paths"]:
            path = path.replace("~", os.path.expanduser('~'))
            for z, v in config["Directory"][k]["files"].items():
                if "file_patern" in config["Directory"][k]["files"][z]:
                    if "sort_path" in config["Directory"][k]["files"][z]:
                        do_list(path, config["Directory"][k]["files"][z]["file_patern"], config["Directory"][k]["files"][z]["command"], config["Directory"][k]["files"][z]["sort_path"])
                    else:
                        do_list(path, config["Directory"][k]["files"][z]["file_patern"], config["Directory"][k]["files"][z]["command"])
