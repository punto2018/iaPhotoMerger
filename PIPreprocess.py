from PILogger import logger
import multiprocessing
import threading
from PIThread import PIThread
import time

threadCompleted = []
threadPercent = []
loadingTimer = None
threadNum = int(multiprocessing.cpu_count())
lock = threading.Lock()
stopPercent = False


def performPreprocess(myFileArray):
    # if __name__ == "__main__":  # confirms that the code is under main function
    #     logger.info("Parallel processing starting from main thread OK")
    # else:
    #     logger.error("NOT ON  MAIN THREAD "+__name__)
    #     exit(1)
    global stopPercent

    blocksLen = int(len(myFileArray) / threadNum)
    logger.info("Threads: " + str(threadNum) + " each thread will process: " + str(blocksLen))

    for i in range(threadNum):
        threadCompleted.append(0)
        threadPercent.append("0")

    if blocksLen < 1:
        logger.info("Too low files, will use 1 single thread")
        calculateHash(0, 0, len(myFileArray), myFileArray)
    else:
        lastBlockMore = int(len(myFileArray) % threadNum)
        start = 0
        end = blocksLen - 1
        threads = []

        logger.info(threadCompleted)

        for i in range(threadNum):
            thread = PIThread(target=calculateHash, args=(i, start, end, myFileArray))
            threads.append(thread)
            thread.start()

            start = end + 1
            end = start + blocksLen - 1
            if i == (threadNum - 2):
                end = end + lastBlockMore + 1

        # Attesa fino a quando tutti i thread non terminano
        logger.info("All Threads started...")

        logger.debug("Starting show percent")
        stopPercent = False
        percentthread = PIThread(target=showPercent)
        percentthread.start()

        for thread in threads:
            thread.join()
        logger.info("Threads all returned!!!")

        logger.debug("Stopping percent")
        stopPercent = True
        percentthread.join()


        for file in myFileArray:
            if file.date is None:
                logger.info("Finishing file: " + file.path)
                file.parseMetadata()

        for file in myFileArray:
            if file.date is None:
                logger.info("Can parse file: " + file.path)


def calculateHash(threadNum, startIndex, endIndex, myFileArray):
    try:
        totalToProcess = endIndex - startIndex
        logger.debug("\tProcessing files from:" + str(startIndex) + " to: " + str(endIndex))
        completed = 0
        for i in range(startIndex, endIndex):
            #if not SKIP_DUPLICATES:
            myFileArray[i].getHashing()
            myFileArray[i].parseMetadata()
            completed = completed + 1
            lock.acquire()
            formattato = "{:.1f}%".format((completed/totalToProcess)*100)
            threadPercent[threadNum] = formattato
            lock.release()

        threadCompleted[threadNum] = 1
        logger.info("Thread status: " + str(threadCompleted))
    except Exception as e:
        logger.info("Exception: in thread " + str(threadNum) + " " + str(e))


def showPercent():
    global stopPercent
    logger.info("Thread percent: "+str(threadPercent))
    time.sleep(1)
    if not stopPercent:
        showPercent()
    else:
        logger.debug("Stopping percent command")
        return
