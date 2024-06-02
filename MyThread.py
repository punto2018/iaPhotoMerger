from threading import Thread
import traceback
from PILogger import logger

class MyThread(Thread):
    err = None
    def run(self):
        try:
            Thread.run(self)
            logger.debug("Thread completed")
        except Exception as err:
            tb = traceback.format_exc()

            logger.error("Thread error "+str(err)+" "+tb)
            self.err = err
            pass  # or raise err
        else:
            self.err = None
