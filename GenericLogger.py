# -*- encoding utf-8 -*-
import logging


class GenericLogger:
    """
    Generic logger class to provide general functionality for concrete loggers.
    Exists to be extended.
    """

    def __init__(self):
        pass

    def get_logger(self, level, handler):
        """
        Provides a logger instance

        :param level: Log level (String)
        :param handler: Log handler (Handler)
        :return: (Logger)
        """
        logger = logging.getLogger(str(self.__class__))
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    def get_formatter(self):
        """
        Defines the formatting for log entries

        :return: (Formatter)
        """
        formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
        return formatter

