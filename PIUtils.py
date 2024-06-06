from PILogger import logger
import os
import hashlib
import subprocess

def get_hash_by_file(mypath=""):
    func = getattr(hashlib, "md5")()
    f = os.open(mypath, os.O_RDONLY)
    for block in iter(lambda: os.read(f, 2048 * func.block_size), b''):
        func.update(block)
    os.close(f)
    return func.hexdigest()


def execute_command(command):
    logger.debug("Executing command "+command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # Output del comando
    output = result.stdout
    # Output dell'errore (se presente)
    #error = result.stderr
    logger.debug("Output: "+output)
    return output

def parse_date(aLine):
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