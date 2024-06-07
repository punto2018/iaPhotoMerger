from PILogger import logger
from datetime import datetime
import PIUtils


class MediaFile:
    path = ""
    hashing = ""
    camera = ""
    kind = ""
    year = ""
    date = None
    filename = ""
    fullMetadata = ""
    size = 0

    def __repr__(self):
        return f'MediaFile(path={self.path}, hashing={self.hashing}, camera={self.camera}, kind={self.kind}, year={self.year}, date={self.date}, filename={self.filename}, size={self.size})'

    def __init__(self, path=""):
        self.path = path

    def __str__(self):
        return "*" + self.hashing + "*" + self.path + "*" + self.year + "*" + str(self.date) + "*" + self.fullMetadata

    def __hash__(self):
        return hash((self.getHashing()))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.getHashing() == other.getHashing()

    def getHashing(self):
        if len(self.hashing) > 0:
            logger.debug("Returning ready hash")
            return self.hashing

        logger.debug("Calculating hash")
        #md5 = hashlib.md5(open(self.path, 'rb').read()).hexdigest()
        md5 = PIUtils.get_hash_by_file(self.path)
        logger.debug("Calculating hash done")

        if md5 is not None and len(md5) > 0:
            self.hashing = md5
        else:
            logger.error("Error calculating MD5 of " + self.path)
            self.hashing = "0000"
        return self.hashing

    def parseMetadata(self):
        try:
            if self.date is not None:
                logger.debug("Returning already existing data " + self.path)
                return

            logger.debug("Parsing metadata of " + self.path)

            #2024-05-25 11:20:54 +0000
            #parsed_date = datetime.strptime(date_string, date_format)
            datesFound = []

            cmd = 'mdls "%s"' % self.path
            output_a = PIUtils.execute_command(cmd)
            output = output_a.splitlines()

            for line in output:
                if "kMDItemKind" in line:
                    kind = line.split("= ")[1]
                    kind = kind.replace('"', '')
                    self.kind = kind

                if "kMDItemAcquisitionModel" in line:
                    camera = line.split("= ")[1]
                    camera = camera.replace('"', '')
                    self.camera = camera

                if "kMDItemFSName" in line:
                    filename = line.split("= ")[1]
                    filename = filename.replace('"', '')
                    self.filename = filename

                #kMDItemPhysicalSize
                if "kMDItemPhysicalSize" in line:
                    size = line.split("= ")[1]
                    size = size.replace('"', '')
                    self.size = int(size)

                aDate = PIUtils.parse_date(line)

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

            if self.camera is None or len(self.camera) == 0:
                logger.debug("Cant find a valid camera for " + self.path)
                self.camera = "Unknown Camera"

            self.fullMetadata = output_a

        except Exception as e:
            logger.error("EXCEPTION PARSING METADATA " + str(e))

    def getExtension(self):
        try:
            part = self.path.split(".")
            part = part[len(part) - 1].lower()
            if len(part) == 0:
                return "NONE"
            return part
        except Exception as e:
            logger.error("Cant get extension of " + self.path + " with " + e)
            return "NONE"
