import os

if __name__ != "__main__":
    # printing main program process id
    exit(0)
else:
    print("ID of main process: {}".format(os.getpid()))

import sys
import datetime
import subprocess
import concurrent.futures
import time
import traceback
import PIClass
from PIClass import MediaFile
from PILogger import logger
import threading
import time
import multiprocessing
from multiprocessing import Process
import shutil
from pathlib import Path

####
rootdir = "/Volumes/SSD960GB/foto 21-23"
rootdir = "/Users/utente/Documents"
rootdir = "/Users/utente/foto/foto 21-23"
#rootdir = "/Users/utente/Downloads"
rootdir = "/Users/utente/foto/SSD960GB/Foto/Download di Amazon Photos/Immagini/2021"
threadNum = multiprocessing.cpu_count()

####

myFileArray = []
hashesDic = {}
filesByExtensionsDic = {}
totalCameras = {}
totalYears = {}
sourceVolume = rootdir
destinationVolume = "/Users/utente/Documents/DEST"
destinationMidPath = "foto"

def getListOfVolumes():
    obj = os.scandir("/Volumes")
    i = 0
    volumes = []
    for entry in obj:
        if entry.is_dir():
            logger.info("["+str(i)+"] "+entry.path)
            volumes.append(entry.path)
            i = i + 1
    sourceVolumeInput = input("[Source] Insert volume number or path, [r] to reload volumes -> ")
    if(sourceVolumeInput == "r"):
        getListOfVolumes()
        return
    if sourceVolumeInput.isnumeric():
        sourceVolume = volumes[int(sourceVolumeInput)]
    else:
        sourceVolume = sourceVolumeInput
    destinationVolumeInput = input("[Destination] Insert destination volume number or path -> ")
    if destinationVolumeInput.isnumeric():
        destinationVolume = volumes[int(destinationVolumeInput)]
    else:
        destinationVolume = destinationVolumeInput


def walk_file_or_dir(root):
    #print("R " + root)
    obj = os.scandir(root)
    for entry in obj:
        if entry.is_file():
            #print("I " + entry.path)
            loadFile(entry.path)
        elif entry.is_dir():
            walk_file_or_dir(entry.path)

def calculateAllHash_P():
    calculateHash(0, len(myFileArray))


def calculateAllHash():
    if __name__ == "__main__":  # confirms that the code is under main function
        logger.info("On main thread OK")
    else:
        logger.error("NOT ON  MAIN THREAD")
    blocksLen = int(len(myFileArray) / threadNum)
    logger.info("Threads: " + str(threadNum) + " each thread will process: " + str(blocksLen))

    if blocksLen < 1:
        calculateHash(0, len(myFileArray))
    else:
        lastBlockMore = int(len(myFileArray) % threadNum)
        start = 0
        end = blocksLen - 1
        procs = []
        threads = []
        for i in range(threadNum):

            thread = threading.Thread(target=calculateHash, args=(start,end))
            threads.append(thread)
            thread.start()
            #proc = Process(target=calculateHash, args=(start,end))
            #procs.append(proc)
            #proc.start()

            start = end + 1
            end = start + blocksLen - 1
            if i == (threadNum - 2):
                end = end + lastBlockMore + 1

        # Attesa fino a quando tutti i thread non terminano
        for thread in threads:
            thread.join()

        logger.info("Threads all returned!!!")

        for i in myFileArray:
            logger.info(i.year)
            logger.info(i.hashing)


def calculateHash(startIndex, endIndex):
    logger.debug("\tProcessing files from:" + str(startIndex) + " to: " + str(endIndex))
    for i in range(startIndex, endIndex):
        #myFileArray[i].getHashing()
        myFileArray[i].parseMetadata()

       # sys.stdout.write('\r')
       # sys.stdout.flush()
        # Stampa della nuova percentuale di avanzamento
       # sys.stdout.write(f"Progress: {i} files")
       # sys.stdout.flush()


def loadFile(filepath):
    ff = MediaFile(filepath)
    myFileArray.append(ff)
    #sys.stdout.write('\r')
    #sys.stdout.flush()
    # Stampa della nuova percentuale di avanzamento
    #sys.stdout.write(f"Progress: {len(myFileArray)} files")
    #sys.stdout.flush()


def getStats():
   #ESTENSIONE
    for file in myFileArray:
        if len(file.getExtension()) != 0:
            if file.getExtension() in filesByExtensionsDic:
                filesByExtensionsDic[file.getExtension()] = filesByExtensionsDic[file.getExtension()] + 1
            else:
                filesByExtensionsDic[file.getExtension()] = 1
        else:
            logger.error("[ERR] Strange extension found! -> " + file.path)

        if len(file.camera) != 0:
            if file.camera in totalCameras:
                totalCameras[file.camera] = totalCameras[file.camera] + 1
            else:
                totalCameras[file.camera] = 1

        if len(file.year) != 0:
            if file.year in totalYears:
                totalYears[file.year] = totalYears[file.year] + 1
            else:
                totalYears[file.year] = 1


def removeDuplicates():
    global myFileArray

    #METODO 1
    # list_of_tuples = list(map(lambda x: (x, None), myFileArray))
    # print(list_of_tuples)
    # dict_myFileArray = dict(list_of_tuples)
    # print(dict_myFileArray)
    # myFileArray = list(dict_myFileArray.keys())

    #METODO 2
    mySet = set()
    for i in myFileArray:
       mySet.add(i)
    myFileArray = list(mySet)

    # for i in range(0, len(myFileArray)):
    #     file = myFileArray[i]
    #     before = len(hashesDic)
    #     hashesDic[file.getMD5()] = file
    #     after = len(hashesDic)
    #     if before != after:
    #         print("Duplicate file found **" + file.path + "**")
    #
    # myFileArray = list(hashesDic.values())


    #for file in myFileArray:
    #    print("File: " + file.path)


def copyFiles():
    for file in myFileArray:
        try:
            destinationFile = destinationVolume + "/" + destinationMidPath + "/" + file.year + "/" + str(file.date.month)
            destinationFilePath = Path(destinationFile)
            destinationFilePath.mkdir(parents=True, exist_ok=True)
            destinationFile = destinationFile + "/" + file.filename
            logger.info("[Copy] "+file.path+" -> "+destinationFile)
            shutil.copy2(file.path, destinationFile)
        except Exception as e:
            logger.info("Error coping " + file.path + " " + str(e))


#-----------START PROGRAM -----------

if __name__ != "__main__":
    # printing main program process id
    exit(0)
else:
    logger.info("ID of main process: {}".format(os.getpid()))

logger.info("Start from " + rootdir)

logger.info("List of volumes ")
#getListOfVolumes()

##### BLOCK
logger.info("Loading files...")
tic = time.perf_counter()
walk_file_or_dir(rootdir)
toc = time.perf_counter()
logger.info("Loaded " + str(len(myFileArray)) + " files")
logger.info(f"[{toc - tic:0.4f} seconds]")

##### BLOCK
logger.info("Calculating hashes and metadata...")
tic = time.perf_counter()
calculateAllHash()
toc = time.perf_counter()
logger.info("Calculating hashes done")
logger.info(f"[{toc - tic:0.4f} seconds]")

logger.info("Removing duplicates...")
tic = time.perf_counter()
before = len(myFileArray)
removeDuplicates()
after = len(myFileArray)
toc = time.perf_counter()
logger.info("Removed " + str(before - after) + " files")
logger.info(f"[{toc - tic:0.4f} seconds]")

logger.info("-----STATS------")
getStats()

##### BLOCK
logger.info("Filetypes found:")
for totalFile in filesByExtensionsDic:
    logger.info("\t" + totalFile + " = " + str(filesByExtensionsDic[totalFile]))

logger.info("Cameras found:")
for totalCamera in totalCameras:
    logger.info("\t"+totalCamera + " = " + str(totalCameras[totalCamera]))

logger.info("Years found:")
for totalYear in totalYears:
    logger.info("\t"+totalYear + " = " + str(totalYears[totalYear]))

logger.info("Start copy files:")
copyFiles()