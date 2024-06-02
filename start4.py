import os
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
from MyThread import MyThread
import pickle
import hashlib

####
rootdir = "/Volumes/SSD960GB/foto 21-23"
rootdir = "/Users/utente/Documents"
rootdir = "/Users/utente/foto/foto 21-23"
#rootdir = "/Users/utente/Downloads"
rootdir = "/Users/utente/foto/SSD960GB/Foto/Download di Amazon Photos/Immagini/2021"
#rootdir = "/Users/utente/foto/SSD960GB/Foto"
#rootdir = "/Users/utente/foto/SSD960GB/Foto/Download di Amazon Photos/Immagini"
####


#### PARAMS
threadNum = multiprocessing.cpu_count()
destinationVolume = "/Users/utente/Documents/DEST"
destinationMidPath = "foto"
extensionsToCopy_photo = [".jpg", ".bmp", ".jpeg", ".gif", ".png", ".m4a", ".webp", ".heic", ".mov", ".dng", ".mp4"]
extensionsToCopy_docs = [".gif", ".png", ".webp", ".tif", ".mkv", ".avi"]
extensionsToCopy_other = [".nef", ".aae", "txt", ]

md5_hash = lambda s: hashlib.md5(s.encode()).hexdigest()
SKIP_DUPLICATES = True
SKIP_COPY = True
DATA_FILENAME = md5_hash(rootdir)

####

myFileArray = []
myFileDic = {}
filesByExtensionsDic = {}
totalCameras = {}
totalYears = {}
sourceVolume = rootdir
threadCompleted = []
threadPercent = []
loadingTimer = None


def getListOfVolumes():
    obj = os.scandir("/Volumes")
    i = 0
    volumes = []
    for entry in obj:
        if entry.is_dir():
            logger.info("[" + str(i) + "] " + entry.path)
            volumes.append(entry.path)
            i = i + 1
    sourceVolumeInput = input("[Source] Insert volume number or path, [r] to reload volumes -> ")
    if (sourceVolumeInput == "r"):
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
    obj = os.scandir(root)
    for entry in obj:
        if entry.is_file():
            loadFile(entry.path)
        elif entry.is_dir():
            walk_file_or_dir(entry.path)


def calculateAllHash_P():
    calculateHash(0, len(myFileArray))


stopPercent = False
def showPercent():
    logger.info(threadPercent)
    time.sleep(1)
    if not stopPercent:
        showPercent()
    else:
        return

def calculateAllHash():
    if __name__ == "__main__":  # confirms that the code is under main function
        logger.info("Parallel processing starting from main thread OK")
    else:
        logger.error("NOT ON  MAIN THREAD")
    blocksLen = int(len(myFileArray) / threadNum)
    logger.info("Threads: " + str(threadNum) + " each thread will process: " + str(blocksLen))

    if blocksLen < 1:
        logger.info("Too low files, will use 1 single thread")
        calculateHash(0, 0, len(myFileArray))
    else:
        lastBlockMore = int(len(myFileArray) % threadNum)
        start = 0
        end = blocksLen - 1
        threads = []

        for i in range(threadNum):
            threadCompleted.append(0)
            threadPercent.append(0)

        logger.info(threadCompleted)

        for i in range(threadNum):
            thread = MyThread(target=calculateHash, args=(i, start, end))
            threads.append(thread)
            thread.start()

            start = end + 1
            end = start + blocksLen - 1
            if i == (threadNum - 2):
                end = end + lastBlockMore + 1

        # Attesa fino a quando tutti i thread non terminano
        logger.info("All Threads started...")

        #showPercent()

        for thread in threads:
            thread.join()

        #stopPercent = True

        logger.info("Threads all returned!!!")

        for file in myFileArray:
            if file.date is None:
                logger.info("Finishing file: " + file.path)
                file.parseMetadata()

        for file in myFileArray:
            if file.date is None:
                logger.info("Can parse file: " + file.path)

lock = threading.Lock()
def calculateHash(threadNum, startIndex, endIndex):
    try:
        logger.debug("\tProcessing files from:" + str(startIndex) + " to: " + str(endIndex))
        completed = 0
        for i in range(startIndex, endIndex):
            if not SKIP_DUPLICATES:
                myFileArray[i].getHashing()
            myFileArray[i].parseMetadata()
            completed = completed + 1
            lock.acquire()
            threadPercent[threadNum] = completed
            lock.release()

        threadCompleted[threadNum] = 1
        logger.info("Thread status: " + str(threadCompleted))
    except Exception as e:
        logger.info("Exception: in thread " + str(threadNum) + " " + str(e))


def loadFile(filepath):
    ff = MediaFile(filepath)
    myFileArray.append(ff)


def getStats():
    #ESTENSIONE
    for file in myFileArray:
        ext = file.getExtension()
        if len(ext) != 0:
            if ext in filesByExtensionsDic:
                filesByExtensionsDic[ext] = filesByExtensionsDic[ext] + 1
            else:
                filesByExtensionsDic[ext] = 1
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
    if SKIP_DUPLICATES:
        return

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
            destinationFile = destinationVolume + "/" + destinationMidPath + "/" + file.year + "/" + str(
                file.date.month)
            destinationFilePath = Path(destinationFile)
            destinationFilePath.mkdir(parents=True, exist_ok=True)
            destinationFile = destinationFile + "/" + file.filename
            logger.info("[Copy] " + file.path + " -> " + destinationFile)
            shutil.copy2(file.path, destinationFile)
        except Exception as e:
            logger.info("Error coping " + file.path + " " + str(e) + " " + str(file))


def saveData():
    logger.info("Saving data on file " + DATA_FILENAME)
    # Salvare l'array di oggetti su file
    with open(DATA_FILENAME, 'wb') as file:
        pickle.dump(myFileArray, file)

    hashtable = {file.path: file for file in myFileArray}
    with open(DATA_FILENAME + "_ht", 'wb') as file:
        pickle.dump(hashtable, file)


def loadData():
    logger.info("Loading data from file " + DATA_FILENAME)

    if not os.path.exists(DATA_FILENAME):
        return
        # Salvare l'array di oggetti su file
    with open(DATA_FILENAME, 'rb') as file:
        loadedArray = pickle.load(file)

    with open(DATA_FILENAME + "_ht", 'rb') as file:
        hashtable = {}
        hashtable = pickle.load(file)

        if hashtable is not None and len(hashtable) > 0:
            logger.info("Loaded " + str(len(hashtable)) + " entries")

            for i in range(len(myFileArray)):
                if myFileArray[i].path in hashtable:
                    myFileArray[i] = hashtable[myFileArray[i].path]
        else:
            logger.warning("Loaded hash is " + str(hashtable))
            #for loadedFile in loadedArray:
            #    if loadedFile.path == myFileArray[i].path:
            #        myFileArray[i] = loadedFile
            #        continue
    #for file in myFileArray:
    #   if file.date is None:
    #      logger.info("Finishing file: " + file.path)
    #     file.parseMetadata()


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
logger.info("Reading files...")
tic = time.perf_counter()
walk_file_or_dir(rootdir)
toc = time.perf_counter()
logger.info("Read " + str(len(myFileArray)) + " files")
logger.info(f"[{toc - tic:0.4f} seconds]")

logger.info("Loading saved data...")
tic = time.perf_counter()
loadData()
toc = time.perf_counter()
logger.info("Loading data done")
logger.info(f"[{toc - tic:0.4f} seconds]")

##### BLOCK
logger.info("Calculating hashes and metadata...")
tic = time.perf_counter()
calculateAllHash()
toc = time.perf_counter()
logger.info("Calculating hashes done")
logger.info(f"[{toc - tic:0.4f} seconds]")

logger.info("Saving...")
tic = time.perf_counter()
saveData()
toc = time.perf_counter()
logger.info("Saving data done")
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
tic = time.perf_counter()
getStats()
toc = time.perf_counter()
logger.info(f"[{toc - tic:0.4f} seconds]")

##### BLOCK
logger.info("Filetypes found:")
for totalFile in filesByExtensionsDic:
    logger.info("\t" + totalFile + " = " + str(filesByExtensionsDic[totalFile]))

logger.info("Cameras found:")
for totalCamera in totalCameras:
    logger.info("\t" + totalCamera + " = " + str(totalCameras[totalCamera]))

logger.info("Years found:")
for totalYear in totalYears:
    logger.info("\t" + totalYear + " = " + str(totalYears[totalYear]))

if not SKIP_COPY:
    logger.info("Start copy files:")
    copyFiles()
