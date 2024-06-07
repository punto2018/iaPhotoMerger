import os

import PIManager
from PILogger import logger
import time
from PIManager import parseInput
from PIManager import sourceVolume
from PIManager import SKIP_COPY
from PIManager import SKIP_DUPLICATES
from PIManager import CLEAR_DEST
from PIManager import SKIP_LOW_RES
from PIManager import ONLY_LOW_RES



import PILoader
import PIPreprocess
import PIPostprocessing


if __name__ != "__main__":
    exit(1)
else:
    logger.debug("ID of main process: {}".format(os.getpid()))

logger.info("--- START ---")
parseInput()
logger.info("Processing photos from folder: " + sourceVolume)

##### BLOCK
logger.info("Reading files...")
tic = time.perf_counter()
PILoader.searchPhotos(sourceVolume)
toc = time.perf_counter()
logger.info("Read " + str(len(PILoader.myFileArray)) + " files")
logger.info(f"[{toc - tic:0.4f} seconds]")

if not PIManager.SKIP_CACHE:
    ##### BLOCK
    logger.info("Loading saved data...")
    tic = time.perf_counter()
    PILoader.loadData(sourceVolume)
    toc = time.perf_counter()
    logger.info("Loading data done")
    logger.info(f"[{toc - tic:0.4f} seconds]")

##### BLOCK
logger.info("Calculating hashes and metadata...")
tic = time.perf_counter()
PIPreprocess.performPreprocess(PILoader.myFileArray)
toc = time.perf_counter()
logger.info("Calculating hashes done")
logger.info(f"[{toc - tic:0.4f} seconds]")

logger.info("Saving processed data...")
tic = time.perf_counter()
PILoader.saveData(sourceVolume)
toc = time.perf_counter()
logger.info("Saving data done")
logger.info(f"[{toc - tic:0.4f} seconds]")

if not SKIP_DUPLICATES:
    logger.info("Removing duplicates...")
    tic = time.perf_counter()
    PILoader.removeDuplicates()
    toc = time.perf_counter()
    logger.info(f"[{toc - tic:0.2f} seconds]")

logger.info("\n\n-----STATS------")
tic = time.perf_counter()
PIPostprocessing.setPhotoArray(PILoader.myFileArray)
PIPostprocessing.getStats()
toc = time.perf_counter()
logger.info(f"[{toc - tic:0.4f} seconds]")

logger.info("Procedo con i dati sintetizzati nelle statistiche mostrate? [y,n]")
char = input("")
if char != "y":
    exit(1)

if not SKIP_COPY:
    tic = time.perf_counter()
    if CLEAR_DEST:
        logger.info("ATTENZIONE! Tutti i dati in questa cartella verranno cancellati: "+PIManager.destinationVolume)
        logger.info("Continuo? [y,n]")
        char = input("")
        if char != "y":
            exit(1)

        logger.info("Cleaning destination folder...")
        PIPostprocessing.clear_folder(PIManager.destinationVolume)

    logger.info("Start copy files:")

    if not ONLY_LOW_RES:
        PIPostprocessing.copyFiles(PIManager.destinationVolume, PIManager.extensionsToCopy_photo, PIManager.extensionsToCopy_docs)
        PIPostprocessing.copyDocuments(PIManager.destinationVolume, PIManager.extensionsToCopy_docs)
    if not SKIP_LOW_RES:
        PIPostprocessing.generateLowResCopyForPhone_p(PIManager.destinationVolume, PIManager.extensionsToCopy_photo)
        PIPostprocessing.lowResRatio()

    toc = time.perf_counter()
    logger.info(f"[{toc - tic:0.4f} seconds]")