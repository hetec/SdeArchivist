# -*- encoding utf-8 -*-
import arcpy
import os
from sdeException import SdeException


class SdeConnectionGenerator:
    """
    Creates a new SDE connection file to be able to connect to the SDE database
    """

    def __init__(self, properties):
        """
        Creates a new SdeConnectionGenerator instance of a set of properties
        :param properties: Properties which are necessary to build a SDE file (Dictionary)
        :return: new SdeConnectionGenerator instance
        """
        self.__basePath = properties["connection_file_path"] + "/config"
        self.__sdeFileName = "connection.sde"
        self.__sdeFile = self.__basePath + "/" + self.__sdeFileName
        self.__database = properties["database_type"]
        self.__instance = properties["instance_name"]
        self.__authMethod = properties["auth_method"]
        self.__username = properties["username"]
        self.__password = properties["password"]

    def __check_existence_of_sde_file(self):
        if os.path.isfile(self.__sdeFile) and os.access(self.__sdeFile, os.R_OK):
            return 1
        else:
            return 0
             
    def __create_new_sde_connection_file(self):
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
        """
        if self.__check_existence_of_sde_file():
            print("File does already exist --> use existing one")
        else:
            print "Create NEW sde file"
            try:
                self.__create_new_sde_connection_file()
            except arcpy.ExecuteError:
                m = "Can`t find existing sde file or create a new one to connect to database for:"
                m = m + " SDE File: " + self.__sdeFile
                m = m + " User: " + self.__username
                m = m + " Password: " + self.__password
                m += " Please check your configuration data and database connection."
                raise SdeException(m)
