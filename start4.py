import os

import PIManager
from PILogger import logger
import time
from PIManager import parseInput
from PIManager import rootdir
from PIManager import SKIP_COPY
from PIManager import SKIP_DUPLICATES
from PIManager import CLEAR_DEST

import PILoader
import PIPreprocess
import PIPostprocessing


if __name__ != "__main__":
    exit(1)
else:
    logger.debug("ID of main process: {}".format(os.getpid()))

parseInput()

logger.info("Processing photos from folder: " + rootdir)

##### BLOCK
logger.info("Reading files...")
tic = time.perf_counter()
PILoader.searchPhotos(rootdir)
toc = time.perf_counter()
logger.info("Read " + str(len(PILoader.myFileArray)) + " files")
logger.info(f"[{toc - tic:0.4f} seconds]")

if not PIManager.SKIP_CACHE:
    ##### BLOCK
    logger.info("Loading saved data...")
    tic = time.perf_counter()
    PILoader.loadData(rootdir)
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
PILoader.saveData(rootdir)
toc = time.perf_counter()
logger.info("Saving data done")
logger.info(f"[{toc - tic:0.4f} seconds]")

if not SKIP_DUPLICATES:
    logger.info("Removing duplicates...")
    tic = time.perf_counter()
    PILoader.removeDuplicates()
    toc = time.perf_counter()
    logger.info(f"[{toc - tic:0.2f} seconds]")

logger.info("-----STATS------")
tic = time.perf_counter()
PIPostprocessing.setPhotoArray(PILoader.myFileArray)
PIPostprocessing.getStats()
toc = time.perf_counter()
logger.info(f"[{toc - tic:0.4f} seconds]")

if not SKIP_COPY:
    tic = time.perf_counter()
    if CLEAR_DEST:
        logger.info("Cleaning destination folder...")
        PIPostprocessing.clear_folder(PIManager.destinationVolume)

    logger.info("Start copy files:")
    PIPostprocessing.copyFiles(PIManager.destinationVolume, PIManager.extensionsToCopy_photo, PIManager.extensionsToCopy_docs)

    PIPostprocessing.copyDocuments(PIManager.destinationVolume, PIManager.extensionsToCopy_docs)

    PIPostprocessing.generateLowResCopyForPhone_p(PIManager.destinationVolume, PIManager.extensionsToCopy_photo)

    PIPostprocessing.lowResRatio()


    toc = time.perf_counter()
    logger.info(f"[{toc - tic:0.4f} seconds]")