from cbp.exception import HousingException
from cbp.logger import logging
import sys

try:
    logging.info("Logging is working and we are in try block")
    raise Exception("This is trial Exception")
except Exception as e:
    # logging.INFO("loggin in Except block")
    raise HousingException(e, sys) from e