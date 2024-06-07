import sys
import hashlib
from PILogger import logger

rootdir = "/Volumes/SSD960GB/foto 21-23"
rootdir = "/Users/utente/Documents"
rootdir = "/Users/utente/foto/foto 21-23"
#rootdir = "/Users/utente/Downloads"
rootdir = "/Users/utente/foto/SSD960GB/Foto/Download di Amazon Photos/Immagini/2021"
#rootdir = "/Users/utente/foto/SSD960GB/Foto"
#rootdir = "/Users/utente/foto/SSD960GB/Foto/Download di Amazon Photos/Immagini"
rootdir = "/Users/valerio/foto"

#### PARAMS
destinationVolume = "/Users/valerio/dest"
extensionsToCopy_photo = ["jpg", "jpeg", "m4a", "heic", "mov", "dng", "mp4", "hevc"]
extensionsToCopy_docs = ["gif", "png", "webp", "tif", "mkv", "avi", "bmp"]

SKIP_DUPLICATES = True
SKIP_COPY = False
SKIP_CACHE = False
CLEAR_DEST = True

myFileDic = {}


def parseInput():
    global rootdir
    global destinationVolume
    global SKIP_DUPLICATES
    global SKIP_COPY

    if len(sys.argv) <= 1:
        logger.info("No arguments")
    else:

        for i in range[1:len(sys.argv)]:
            if sys.argv[i] == "-i":
                rootdir = sys.argv[i + 1]
            if sys.argv[i] == "-d":
                destinationVolume = sys.argv[i + 1]
            if sys.argv[i] == "-sd":
                SKIP_DUPLICATES = True
            if sys.argv[i] == "-sc":
                SKIP_COPY = True

    logger.info("Input folder: "+rootdir)
    logger.info("Output folder: "+destinationVolume)
    logger.info("SKIP_DUPLICATES: "+str(SKIP_DUPLICATES))
    logger.info("SKIP_COPY: "+str(SKIP_COPY))