# -*- encoding utf-8 -*-
import logging
from ConsoleLogger import ConsoleLogger
from RotatingFileLogger import RotatingFileLogger
import SdeArchivistProperties


class ArchivisLogger:
    def __init__(self, log_properties):
        self.__level = log_properties['level']
        self.__file = log_properties['file']
        self.__max_bytes = log_properties['log_file_size']
        self.__backup_files = log_properties['log_file_count']

    def get_console_logger(self):
        c = ConsoleLogger()
        f = c.get_formatter()
        h = c.get_handler(self.__level, f)
        return c.get_logger(self.__level, h)

    def get_file_logger(self):
        a = RotatingFileLogger()
        f = a.get_formatter()
        h = a.get_file_handler(self.__level, f, self.__file, self.__max_bytes, self.__backup_files)
        return a.get_logger(self.__level, h)

if __name__ == "__main__":
    pass