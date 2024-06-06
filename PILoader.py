from PIMediaClass import MediaFile
import os

myFileArray = []


def walk_file_or_dir(root):
    obj = os.scandir(root)
    for entry in obj:
        if entry.is_file():
            loadFile(entry.path)
        elif entry.is_dir():
            walk_file_or_dir(entry.path)

def loadFile(filepath):
    ff = MediaFile(filepath)
    myFileArray.append(ff)


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



def saveData():
    logger.info("Saving data on file " + DATA_FILENAME)
    # Salvare l'array di oggetti su file
    with open(DATA_FILENAME, 'wb') as file:
        pickle.dump(myFileArray, file)

    hashtable = {file.path: file for file in myFileArray}
    with open(DATA_FILENAME + "_ht", 'wb') as file:
        pickle.dump(hashtable, file)
