from PILogger import logger

filesByExtensionsDic = {}
totalCameras = {}
totalYears = {}

myFileArray = []


def setPhotoArray(theArray):
    global myFileArray
    myFileArray = theArray


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
