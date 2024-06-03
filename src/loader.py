import logging
import sys

from components.database import DB

db = DB()

log_format = '%(asctime)s|%(levelname)-5s|%(filename)-14s|%(funcName)-10s|%(message)s'
logging.basicConfig(level=10, format=log_format, datefmt='%H:%M:%S', stream=sys.stdout)
