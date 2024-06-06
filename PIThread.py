from threading import Thread
import traceback
from PILogger import logger

<<<<<<< HEAD:PIThread.py
class PIThread(Thread):
=======


class MyThread(Thread):
>>>>>>> 344a0568ab92dc5c7e1fcb3c6c23e4cdee54ff72:MyThread.py
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
