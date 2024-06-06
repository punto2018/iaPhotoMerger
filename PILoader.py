from PIMediaClass import MediaFile
import os
from PILogger import logger
import hashlib
import pickle

myFileArray = []
md5_hash = lambda s: hashlib.md5(s.encode()).hexdigest()


def searchPhotos(root):
    if not os.path.exists(root):
        logger.error("Path does not exist: " + root)
        exit(1)

    obj = os.scandir(root)
    for entry in obj:
        if entry.is_file():
            addPhoto(entry.path)
        elif entry.is_dir():
            searchPhotos(entry.path)


def addPhoto(filepath):
    ff = MediaFile(filepath)
    myFileArray.append(ff)


def loadData(rootdir):
    DATA_FILENAME = "data/" + md5_hash(rootdir)

    logger.debug("Loading data from file " + DATA_FILENAME)

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


def saveData(rootdir):
    DATA_FILENAME = "data/" + md5_hash(rootdir)

    try:
        os.makedirs("data/")
    except FileExistsError:
        pass

    logger.info("Saving data on file " + DATA_FILENAME)
    # Salvare l'array di oggetti su file
    with open(DATA_FILENAME, 'wb') as file:
        pickle.dump(myFileArray, file)

    hashtable = {file.path: file for file in myFileArray}
    with open(DATA_FILENAME + "_ht", 'wb') as file:
        pickle.dump(hashtable, file)


def removeDuplicates():
    global myFileArray

    before = len(myFileArray)

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

    after = len(myFileArray)
    logger.info("Removed " + str(before - after) + " files")

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
