# -*- encoding utf-8 -*-
import logging
from ConsoleLogger import ConsoleLogger
from RotatingFileLogger import RotatingFileLogger


class ArchivisLogger:
    def __init__(self, log_properties):
        self.__level = logging.WARNING
        self.__check_level(log_properties['level'])
        self.__file = log_properties['file']

    def __check_level(self, level):
        l = str(level).lower()
        if l == "debug":
            self.__level = logging.DEBUG
        elif l == "info":
            self.__level = logging.INFO
        elif l == "warn":
            self.__level = logging.WARNING
        elif l == "error":
            self.__level = logging.ERROR
        elif l == "fatal":
            self.__level = logging.FATAL


    def get_console_logger(self):
        c = ConsoleLogger()
        f = c.get_formatter()
        h = c.get_handler(self.__level, f)
        return c.get_logger(self.__level, h)

    def get_file_logger(self):
        a = RotatingFileLogger()
        f = a.get_formatter()
        h = a.get_file_handler(self.__level, f, self.__file)
        return a.get_logger(self.__level, h)


