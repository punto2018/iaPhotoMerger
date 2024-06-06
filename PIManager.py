import multiprocessing
import sys

rootdir = "/Volumes/SSD960GB/foto 21-23"
rootdir = "/Users/utente/Documents"
rootdir = "/Users/utente/foto/foto 21-23"
#rootdir = "/Users/utente/Downloads"
rootdir = "/Users/utente/foto/SSD960GB/Foto/Download di Amazon Photos/Immagini/2021"
#rootdir = "/Users/utente/foto/SSD960GB/Foto"
#rootdir = "/Users/utente/foto/SSD960GB/Foto/Download di Amazon Photos/Immagini"

#### PARAMS
threadNum = multiprocessing.cpu_count()
destinationVolume = "/Users/utente/Documents/DEST"
destinationMidPath = "foto"
extensionsToCopy_photo = [".jpg", ".bmp", ".jpeg", ".gif", ".png", ".m4a", ".webp", ".heic", ".mov", ".dng", ".mp4"]
extensionsToCopy_docs = [".gif", ".png", ".webp", ".tif", ".mkv", ".avi"]
extensionsToCopy_other = [".nef", ".aae", "txt"]

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


def parseInput():

    if len(sys.argv) <= 1:
        print("No arguments")
        return

    for i in range[1:len(sys.argv)]:
        if sys.argv[i] == "-i":
            rootdir = sys.argv[i + 1]
            DATA_FILENAME = md5_hash(rootdir)
        if sys.argv[i] == "-d":
            destinationVolume = sys.argv[i + 1]
        if sys.argv[i] == "-sd":
            SKIP_DUPLICATES = True
        if sys.argv[i] == "-sc":
            SKIP_COPY = True
