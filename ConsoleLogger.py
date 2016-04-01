# -*- encoding utf-8 -*-
import logging
from GenericLogger import GenericLogger


class ConsoleLogger(GenericLogger):
    """
    Configures and create a StreamHandler instance
    """

    def __init__(self):
        pass

    def get_handler(self, level, formatter):
        """
        Configures and create a  StreamHandler instance

        :param level: The log level (String)
        :param formatter: The formatter instance (Formatter)
        :return: StreamHandler
        """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        return console_handler


