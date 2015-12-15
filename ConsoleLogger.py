# -*- encoding utf-8 -*-
import logging
from GenericLogger import GenericLogger


class ConsoleLogger(GenericLogger):
    def __init__(self):
        pass

    def get_handler(self, level, formatter):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        return console_handler


