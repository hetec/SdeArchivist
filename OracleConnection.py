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


    def connection(self):
        """
        Returns a connection to the defined oracle database
        :return: cx_Oracle connection object
        """
        url = cx_Oracle.makedsn(self.__db_props["url"], self.__db_props["port"], self.__db_props["service"])
        connection = cx_Oracle.connect(self.__db_props["username"], self.__db_props["password"], url)
        return connection
