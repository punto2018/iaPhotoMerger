import shutil
import time
from pathlib import Path
from PIL import Image
import pillow_heif
import os
from pillow_heif import register_heif_opener

from PILogger import logger

filesByExtensionsDic = {}
totalCameras = {}
totalYears = {}

myFileArray = []


def setPhotoArray(theArray):
    global myFileArray
    myFileArray = theArray
    register_heif_opener()

def getStats():
    #ESTENSIONE

    totalSize = 0

    for file in myFileArray:
        ext = file.getExtension()

        totalSize = totalSize + file.size

        if ext in filesByExtensionsDic:
            filesByExtensionsDic[ext] = filesByExtensionsDic[ext] + 1
        else:
            filesByExtensionsDic[ext] = 1

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

    formattato = "{:.2f}".format(totalSize / 1024 / 1024 / 1024)

    logger.info("TOTAL SIZE: " + formattato + " GB")


def clear_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
    except:
        logger.info("Nothing to delete in " + folder_path)


def copyFiles(destinationVolume, imgExtenesions, docExtensions):
    for file in myFileArray:
        logger.debug("Extension is: " + file.getExtension())

        if file.getExtension() in imgExtenesions:
            try:
                destinationFile = destinationVolume + "/" + file.year + "/" + file.camera + "/" + str(file.date.month)
                destinationFilePath = Path(destinationFile)
                destinationFilePath.mkdir(parents=True, exist_ok=True)
                destinationFile = destinationFile + "/" + file.filename
                logger.info("[Copy IMG] " + file.path + " -> " + destinationFile)
                shutil.copy2(file.path, destinationFile)
            except Exception as e:
                logger.info("Error coping " + file.path + " " + str(e) + " " + str(file))
        elif file.getExtension() not in docExtensions:
            try:
                destinationFile = destinationVolume + "/" + file.year + "/" + "OTHER" + "/" + str(file.date.month)
                destinationFilePath = Path(destinationFile)
                destinationFilePath.mkdir(parents=True, exist_ok=True)
                destinationFile = destinationFile + "/" + file.filename
                logger.info("[Copy OTHER] " + file.path + " -> " + destinationFile)
                shutil.copy2(file.path, destinationFile)
            except Exception as e:
                logger.info("Error coping " + file.path + " " + str(e) + " " + str(file))


def copyDocuments(destinationVolume, docExtensions):
    for file in myFileArray:
        if file.getExtension() in docExtensions:
            try:
                destinationFile = destinationVolume + "/" + file.year + "/" + "DOCS" + "/" + str(file.date.month)
                destinationFilePath = Path(destinationFile)
                destinationFilePath.mkdir(parents=True, exist_ok=True)
                destinationFile = destinationFile + "/" + file.filename
                logger.info("[Copy DOC] " + file.path + " -> " + destinationFile)
                shutil.copy2(file.path, destinationFile)
            except Exception as e:
                logger.info("Error coping " + file.path + " " + str(e) + " " + str(file))


def generateLowResCopyForPhone(destinationVolume, imgExtenesions):
    for file in myFileArray:
        try:
            if file.getExtension() in imgExtenesions:
                destinationFile = destinationVolume + "/" + file.year + "/" + "LOW_RES" + "/" + str(file.date.month)
                destinationFilePath = Path(destinationFile)
                destinationFilePath.mkdir(parents=True, exist_ok=True)

                input_jpeg_path = file.path
                destinationFile = destinationFile + "/lr_" + file.filename + ".heic"
                logger.info("[Low Res] " + file.path + " -> " + destinationFile)

                # RISOLUZIONE DELL IOHONE 2778 x 1284 pixels
                resize_and_convert_to_heic(input_jpeg_path, destinationFile)

        except Exception as e:
            logger.info("Error generating lr " + file.path + " " + str(e))


def resize_and_convert_to_heic(input_path, output_path):
    try:

        # Apri l'immagine con Pillow
        logger.debug("Opening image")
        tic = time.perf_counter()
        img = Image.open(input_path)
        toc = time.perf_counter()
        logger.info(f"[{toc - tic:0.4f} seconds]")

        base_width = int(img.size[0]/3)
        wpercent = (base_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        size = (base_width, hsize)


        # Ridimensiona l'immagine utilizzando l'algoritmo LANCZOS
        logger.debug("Resizing image")
        tic = time.perf_counter()
        img_resized = img.resize(size, Image.LANCZOS)
        toc = time.perf_counter()
        logger.info(f"[{toc - tic:0.4f} seconds]")

        logger.debug("Generating heif")
        tic = time.perf_counter()
        heif_file = pillow_heif.from_pillow(img_resized)
        toc = time.perf_counter()
        logger.info(f"[{toc - tic:0.4f} seconds]")

        logger.debug("Saving heif")
        tic = time.perf_counter()
        heif_file.save(output_path, quality=60)
        toc = time.perf_counter()
        logger.info(f"[{toc - tic:0.4f} seconds]")
        logger.debug("Done")

    except Exception as e:
        logger.error("Cant generate heif "+str(e))
