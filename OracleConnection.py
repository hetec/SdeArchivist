# -*- encoding utf-8 -*-
import cx_Oracle


class OracleConnection:
    """
    Establishes and returns a connection to the defined oracle database.
    For each call of connection() a new connection is established.
    Lazy initialization and reusing of a created connection object
    is ignored since the connection object will be used just once
    """

    def __init__(self, properties):
        self.__db_props = properties

    def set_console_logger(self, console_logger):
        self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        self.__f_logger = file_logger

    def connection(self):
        """
        Returns a connection to the defined oracle database

        :return: cx_Oracle connection object
        """
        try:
            url = cx_Oracle.makedsn(self.__db_props["url"], self.__db_props["port"], self.__db_props["service"])
            connection = cx_Oracle.connect(self.__db_props["username"], self.__db_props["password"], url)
            return connection
        except Exception as e:
            self.__c_logger.exception("Exception while connection to ORACLE: " + str(e))
            self.__f_logger.exception("Exception while connection to ORACLE: " + str(e))
            raise Exception("Exception while connection to ORACLE: " + str(e))
