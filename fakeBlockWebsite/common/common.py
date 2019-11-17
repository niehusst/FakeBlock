import logging
import sys
from logging.handlers import RotatingFileHandler

#Credit to Son Nguyen Kim for logging patterns
#https://www.toptal.com/python/in-depth-python-logging
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "logs/fake_block_server.log"

def get_console_handler():
	# handler for printing to stdout
	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(FORMATTER)
	return console_handler

def get_file_handler():
	# handler for writing logs to file
	# start a new file if the old one hits maxBytes
	file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=1)
	file_handler.setFormatter(FORMATTER)
	return file_handler

def get_logger(logger_name):
	logger = logging.getLogger(logger_name)
	logger.setLevel(logging.DEBUG) # better to have too much log than not enough
	logger.addHandler(get_console_handler())
	logger.addHandler(get_file_handler())
	# with this pattern, it's rarely necessary to propagate the error up to parent
	logger.propagate = False
	return logger


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]