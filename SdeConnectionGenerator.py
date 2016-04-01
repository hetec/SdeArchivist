# -*- encoding utf-8 -*-
import arcpy
import os
from sdeException import SdeException


class SdeConnectionGenerator:
    """
    Creates a new SDE connection file to be able to connect to the SDE database
    """

    def __init__(self, properties, connection_name):
        """
        Creates a new SdeConnectionGenerator instance of a set of properties

        :param properties: Properties which are necessary to build a SDE file (Dictionary)
        :param connection_name: Name of the connection (String)
        :return: new SdeConnectionGenerator instance
        """
        self.__basePath = properties["project_root"] + "/config"
        self.__sdeFileName = str(connection_name) + ".sde"
        self.__sdeFile = self.__basePath + "/" + self.__sdeFileName
        self.__database = properties["database_type"]
        self.__instance = properties["instance_name"]
        self.__authMethod = properties["auth_method"]
        self.__username = properties["username"]
        self.__password = properties["password"]

    def set_console_logger(self, console_logger):
            self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        self.__f_logger = file_logger

    def __check_existence_of_sde_file(self):
        if os.path.isfile(self.__sdeFile) and os.access(self.__sdeFile, os.R_OK):
            return 1
        else:
            return 0
    def __create_new_sde_connection_file(self):
        self.__c_logger.info("CREATE SDE FILE")
        self.__f_logger.info("CREATE SDE FILE")
        arcpy.CreateDatabaseConnection_management(self.__basePath,
                                                  self.__sdeFileName,
                                                  self.__database,
                                                  self.__instance,
                                                  self.__authMethod,
                                                  self.__username,
                                                  self.__password
                                                  )

    def connect(self):
        """
        Handles the creation of the SDE connection file

        - If no connection file exists in /config a new one will be created
        - If a connection file exists in /config it will be reused

        :exception SdeException
        """
        self.__c_logger.info("SDE CONNECTION PROPERTIES: \n"
                             + self.__sdeFile + "\n"
                             + self.__database + "\n"
                             + self.__instance + "\n"
                             + self.__authMethod + "\n"
                             + self.__username + "\n")
        self.__f_logger.info("SDE CONNECTION PROPERTIES: \n"
                             + self.__sdeFile + "\n"
                             + self.__database + "\n"
                             + self.__instance + "\n"
                             + self.__authMethod + "\n"
                             + self.__username + "\n")

        if self.__check_existence_of_sde_file():
            self.__c_logger.info("Sde " + self.__sdeFile + " file already exists")
            self.__f_logger.info("Sde " + self.__sdeFile + " file already exists")
        else:
            try:
                self.__create_new_sde_connection_file()
            except arcpy.ExecuteError:
                m = "Can`t find existing sde file or create a new one to connect to database for:"
                m = m + " SDE File: " + self.__sdeFile
                m = m + " User: " + self.__username
                m = m + " Password: " + self.__password
                m += " Please check your configuration data and database connection."
                self.__c_logger.exception("EXCEPTION WHILE CREATING SDE FILE: " + str(m))
                self.__f_logger.exception("EXCEPTION WHILE CREATING SDE FILE: " + str(m))
                raise SdeException(m)
