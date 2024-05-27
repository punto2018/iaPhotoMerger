import hashlib
import subprocess
import logging
from PILogger import logger
from datetime import datetime


class MediaFile:
    date_format = "%Y-%m-%d %H:%M:%S %z"

    path = ""
    hashing = ""
    creationDateStr = ""
    camera = ""
    kind = ""
    year = ""
    date = None
    filename = ""

    def __init__(self, path=""):
        #logger.debug("Initing a new object")
        self.path = path

    #def __str__(self):
    #   return "*"+self.md5+"*"+self.path+"*"+self.

    def __hash__(self):
        return hash((self.getHashing()))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.getHashing() == other.getHashing()

    def getHashing(self):
        if len(self.hashing) > 0:
            logger.debug("Returning ready hash")
            return self.hashing

        #cmd = "md5 -q '%s'" % self.path
        #output = subprocess.(cmd, shell=True)
        #md5 = output.decode("ascii")

        md5 = hashlib.md5(open(self.path, 'rb').read()).hexdigest()

        if len(md5) > 0:
            logger.debug("Calculating hash " + md5)
            #traceback.print_stack(file=sys.stdout)
            self.hashing = md5
        else:
            logger.error("Error calculating MD5 of " + self.path)
        return self.hashing

    def executeCommand(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # Output del comando
        output = result.stdout
        # Output dell'errore (se presente)
        #error = result.stderr
        logger.debug(output)
        return output

    def parseMetadata(self):
        try:
            logger.debug("Parsing metadata of " + self.path)

            self.getHashing()

            #2024-05-25 11:20:54 +0000
            #parsed_date = datetime.strptime(date_string, date_format)
            datesFound = []
            date_format = self.date_format

            cmd = "mdls '%s'" % self.path
            output_a = self.executeCommand(cmd)
            output = output_a.splitlines()

            for l in output:
                if "kMDItemKind" in l:
                    kind = l.split("= ")[1]
                    kind = kind.replace('"', '')
                    self.kind = kind

                if "kMDItemAcquisitionModel" in l:
                    camera = l.split("= ")[1]
                    camera = camera.replace('"', '')
                    self.camera = camera

                if "kMDItemFSName" in l:
                    filename = l.split("= ")[1]
                    filename = filename.replace('"', '')
                    self.filename = filename

                aDate = self.parseDate(l)
                if aDate != None:
                    datesFound.append(aDate)

            #GESTIONE DATA
            if len(datesFound) > 0:
                self.date = min(datesFound)
                self.creationDateStr = self.date.strftime(date_format)
                if len(self.creationDateStr) == 0:
                    logger.error("ERRORE DATA DI CREAZIONE NON TROVATA: " + output_a)
                    self.year = "1700"
                else:
                    self.year = str(self.date.year)
            else:
                logger.info("Cant find a valid date for " + self.path + " with " + output_a)

            if self.date is None:
                logger.info("Cant find a valid date for " + self.path + " with " + output_a)


        except Exception as e:
            logger.error("EXCEPTION PARSING METADATA " + e)

    def getExtension(self):
        return self.path.split(".")[1]

    def parseDate(self, aLine):

        try:
            if len(aLine) > 0:
                datetime_str = aLine.split("= ")[1]
                datetime_str = datetime_str.replace('"', '')
                if len(datetime_str) > 0:
                    aValidDate = datetime.strptime(datetime_str, self.date_format)
                    return aValidDate
        except Exception as e:
            #logger.error("Cant parse "+aLine)
            return None
