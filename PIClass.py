import hashlib
import subprocess
import logging
from PILogger import logger
from datetime import datetime
import os

class MediaFile:
    date_format = "%Y-%m-%d %H:%M:%S %z"

    path = ""
    hashing = ""
    camera = ""
    kind = ""
    year = ""
    date = None
    filename = ""
    fullMetadata = ""

    def __repr__(self):
        return f'MediaFile(path={self.path}, hashing={self.hashing}, camera={self.camera}, kind={self.kind}, year={self.year}, date={self.date},filename={self.filename})'

    def __init__(self, path=""):
        self.path = path

    def __str__(self):
       return "*"+self.hashing+"*"+self.path+"*"+self.year+"*"+str(self.date)+"*"+self.fullMetadata

    def __hash__(self):
        return hash((self.getHashing()))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.getHashing() == other.getHashing()

    def get_hash(self, mypath=""):
        func = getattr(hashlib, "md5")()
        f = os.open(mypath, os.O_RDONLY)
        for block in iter(lambda: os.read(f, 2048 * func.block_size), b''):
            func.update(block)
        os.close(f)
        return func.hexdigest()

    def getHashing(self):
        if len(self.hashing) > 0:
            logger.debug("Returning ready hash")
            return self.hashing

        logger.debug("Calculating hash")
        #md5 = hashlib.md5(open(self.path, 'rb').read()).hexdigest()
        md5 = self.get_hash(self.path)
        logger.debug("Calculating hash done")

        if md5 is not None and len(md5) > 0:
            self.hashing = md5
        else:
            logger.error("Error calculating MD5 of " + self.path)
            self.hashing = "0000"

        return self.hashing

    def executeCommand(self, command):
        logger.debug("Executing command "+command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # Output del comando
        output = result.stdout
        # Output dell'errore (se presente)
        #error = result.stderr
        logger.debug("Output: "+output)
        return output

    def parseMetadata(self):
        try:
            if self.date is not None:
                logger.debug("Returning already existing data " + self.path)
                return

            logger.debug("Parsing metadata of " + self.path)

            #2024-05-25 11:20:54 +0000
            #parsed_date = datetime.strptime(date_string, date_format)
            datesFound = []
            date_format = self.date_format

            cmd = 'mdls "%s"' % self.path
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
                if aDate is not None:
                    logger.debug("Appending a new date " + str(aDate))
                    datesFound.append(aDate)

            if datesFound is not None and len(datesFound) > 0:
                self.date = min(datesFound)
                logger.debug("Min date is " + str(self.date))

                if self.date is None:
                    logger.error("ERRORE DATA DI CREAZIONE NON TROVATA: " + output_a)
                    self.year = "1700"
                    logger.debug("Cant get year ")
                else:
                    self.year = str(self.date.year)

            else:
                logger.error("Cant find a valid date for " + self.path + " with " + output_a)

            self.fullMetadata = output_a

        except Exception as e:
            logger.error("EXCEPTION PARSING METADATA " + str(e))

    def getExtension(self):
        try:
            part = self.path.split(".")
            return part[len(part) - 1].lower()
        except Exception as e:
            return "NONE"

    def parseDate(self, aLine):
        try:
            if aLine is not None and len(aLine) > 0:
                datetime_str = aLine.split("= ")[1]
                datetime_str = datetime_str.replace('"', '')
                if len(datetime_str) > 0:
                    aValidDate = datetime.strptime(datetime_str, self.date_format)
                    return aValidDate
            return None
        except Exception as e:
            return None
