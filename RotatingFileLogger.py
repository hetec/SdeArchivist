# -*- encoding utf-8 -*-
import logging.handlers
from GenericLogger import GenericLogger

class RotatingFileLogger(GenericLogger):
    def __init__(self):
        pass

    def get_file_handler(self, level, formatter, file, max_bytes, backup_files):
        console_handler = logging.handlers.RotatingFileHandler(filename=file,
                                                               maxBytes=max_bytes,
                                                               backupCount=backup_files)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        return console_handler
