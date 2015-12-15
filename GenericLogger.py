# -*- encoding utf-8 -*-
import logging


class GenericLogger:
    def __init__(self):
        pass

    def get_logger(self, level, handler):
        logger = logging.getLogger(str(self.__class__))
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    def get_formatter(self):
        formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
        return formatter

