import os
import shutil

# Terminal colors
CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CEND = '\033[0m'

# Check if config files has a list of directories to sort
dirList = []
try:
    with open("./FileSorter.config", "r") as config:
        dirList = config.readlines()

    truncatedDirList = []
    for line in dirList:
        truncatedDirList.append(line.split('\n')[0])
    dirList= truncatedDirList

except Exception as e: 
    print("INFO:    No config file with directories found.")

if (len(dirList) == 0 ):
    dirList.append("./")

for directoryText in dirList:
    directory = os.fsencode(directoryText)
    # Throw warning if directory wasn't found
    if (not os.path.isdir(directory)):
        print(CYELLOW+"WARNING:  Directory '"+directoryText+"' was not found."+CEND)
        continue
    
    folders = {}
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # Skip over the config file
        if (filename == "FileSorter.config" or filename == "FileSorter.py"):
            continue

        filenameSplit = filename.split(".")

        # We know this is a file
        if (len(filenameSplit) > 1):    
            extension = filenameSplit[-1]
            print("INFO:    File '"+filename+"' is of type: "+extension)

            # Make sub-directory if it doesn't already exist
            if (extension.lower() not in folders):
                folders[extension.lower()] = True
                try:
                    os.mkdir(directoryText+'/'+extension.lower())
                    print("INFO:    Created folder: "+directoryText+'/'+extension.lower())
                except FileExistsError:
                    folders[extension.lower()] = True
                    print("INFO:    Folder aready exists: "+directoryText+'/'+extension.lower())
                except Exception as e:
                    print(e)

            # Move file to its respective sub-directory
            try:
                shutil.move(directoryText+'/'+filename, directoryText+'/'+extension.lower()+'/'+filename)
                print(CGREEN+"Successfully moved "+directoryText+'/'+filename+" to "+directoryText+'/'+extension.lower()+'/'+filename+CEND)
            except PermissionError:
                print(CRED+"ERROR:  File '"+filename+"' failed to be moved due to a lack of permissions. Make sure this file isn't open in another program!"+CEND)
                print(e)
            except Exception as e:
                print(CRED+"ERROR:  File '"+filename+"' failed to be moved: "+CEND)
                print(e)

        # We know this is a folder
        else:
            print("INFO:    Found existing folder: "+filename)
            if (filename.lower() not in folders):
                folders[filename.lower()] = True
    