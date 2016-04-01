# -*- encoding utf-8 -*-
import logging.handlers
from GenericLogger import GenericLogger

class RotatingFileLogger(GenericLogger):
    """
    Configures and creates a RotatingFileHandler
    """
    def __init__(self):
        pass

    def get_file_handler(self, level, formatter, file, max_bytes, backup_files):
        """
        Configures and creates a RotatingFileHandler

        :param level: Log level (String)
        :param formatter: Formatter instance (Formatter)
        :param file: Path to the log file (String)
        :param max_bytes: Max size of log file in bytes (Integer)
        :param backup_files: Max number of backed up files (Integer)
        :return: RotatingFileHandler
        """
        console_handler = logging.handlers.RotatingFileHandler(filename=file,
                                                               maxBytes=max_bytes,
                                                               backupCount=backup_files)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        return console_handler
