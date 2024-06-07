import sys
import hashlib
from PILogger import logger

sourceVolume = "/Volumes/SSD960GB/foto 21-23"
sourceVolume = "/Users/utente/Documents"
sourceVolume = "/Users/utente/foto/foto 21-23"
#rootdir = "/Users/utente/Downloads"
sourceVolume = "/Users/utente/foto/SSD960GB/Foto/Download di Amazon Photos/Immagini/2021"
#rootdir = "/Users/utente/foto/SSD960GB/Foto"
#rootdir = "/Users/utente/foto/SSD960GB/Foto/Download di Amazon Photos/Immagini"
sourceVolume = "/Users/valerio/foto"
sourceVolume = "/Users/valerio/Desktop/ex rpvc"

#### PARAMS
destinationVolume = "/Users/valerio/dest"
extensionsToCopy_photo = ["jpg", "jpeg", "m4a", "heic", "mov", "dng", "mp4", "hevc"]
extensionsToCopy_docs = ["gif", "png", "webp", "tif", "mkv", "avi", "bmp"]

SKIP_DUPLICATES = False
SKIP_COPY = False
SKIP_CACHE = False
CLEAR_DEST = True
SKIP_LOW_RES = False


### TODO: verifica duplicati con i file che già sono nella destinazione


def parseInput():
    global sourceVolume
    global destinationVolume
    global SKIP_DUPLICATES
    global SKIP_COPY
    global SKIP_CACHE
    global CLEAR_DEST
    global SKIP_LOW_RES

    if len(sys.argv) <= 1:
        logger.info("No arguments")
    else:

        for i in range[1:len(sys.argv)]:
            if sys.argv[i] == "-i":
                sourceVolume = sys.argv[i + 1]
            if sys.argv[i] == "-d":
                destinationVolume = sys.argv[i + 1]
            if sys.argv[i] == "-sd":
                SKIP_DUPLICATES = True
            if sys.argv[i] == "-sc":
                SKIP_COPY = True
            if sys.argv[i] == "-sh":
                SKIP_CACHE = True
            if sys.argv[i] == "-c":
                CLEAR_DEST = True
            if sys.argv[i] == "-sl":
                SKIP_LOW_RES = True


    logger.info("Input folder: " + sourceVolume)
    logger.info("Output folder: "+destinationVolume)
    logger.info("SKIP_DUPLICATES: "+str(SKIP_DUPLICATES))
    logger.info("SKIP_COPY: "+str(SKIP_COPY))
    logger.info("SKIP_CACHE: "+str(SKIP_CACHE))
    logger.info("CLEAR_DEST: "+str(CLEAR_DEST))
    logger.info("SKIP_LOW_RES: "+str(SKIP_LOW_RES))
    logger.info("Photo extensions: "+str(extensionsToCopy_photo))
    logger.info("Docs extensions: "+str(extensionsToCopy_docs))

    logger.info("La configurazione è corretta? [y,n]")
    char = input("")
    if char != "y":
        exit(1)