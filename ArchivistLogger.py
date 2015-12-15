# -*- encoding utf-8 -*-
import logging
from ConsoleLogger import ConsoleLogger
from RotatingFileLogger import RotatingFileLogger


class ArchivistLogger:

    def __init__(self, log_properties):
        self.__level = log_properties['level']
        self.__file = log_properties['file']
        self.__max_bytes = log_properties['log_file_size']
        self.__backup_files = log_properties['log_file_count']
        self.__console_logger = None
        self.__rolling_file_logger = None

    def get_console_logger(self):
        if self.__console_logger is None:
            c = ConsoleLogger()
            f = c.get_formatter()
            h = c.get_handler(self.__level, f)
            self.__console_logger = c.get_logger(self.__level, h)
            return self.__console_logger
        else:
            return self.console_logger

    def get_file_logger(self):
        if self.__rolling_file_logger is None:
            a = RotatingFileLogger()
            f = a.get_formatter()
            h = a.get_file_handler(self.__level, f, self.__file, self.__max_bytes, self.__backup_files)
            self.__rolling_file_logger = a.get_logger(self.__level, h)
            return self.__rolling_file_logger
        else:
            return self.__rolling_file_logger


if __name__ == "__main__":

    pass

    # p = SdeArchivistProperties.SdeArchivistProperties("config/archivist_config.json").log_config
    # a = ArchivisLogger(p)