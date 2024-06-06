import logging
import os

try:
    os.makedirs("log")
except FileExistsError:
    pass

# Creazione del logger
logger = logging.getLogger('esempio_logger')
logger.setLevel(logging.DEBUG)  # Imposta il livello di logging per il logger

# Creazione di un handler per il file con livello DEBUG
file_handler = logging.FileHandler('log/debug.log')
file_handler.setLevel(logging.DEBUG)

# Creazione di un handler per la console con livello INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Creazione di un formatter e aggiunta agli handler
formatter = logging.Formatter('%(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Aggiunta degli handler al logger
#logger.addHandler(file_handler)
logger.addHandler(console_handler)

# # Utilizzo del logger
# logger.debug("Questo è un messaggio di debug")
# logger.info("Questo è un messaggio di info")
# logger.warning("Questo è un messaggio di warning")
# logger.error("Questo è un messaggio di errore")
# logger.critical("Questo è un messaggio critico")