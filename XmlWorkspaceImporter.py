# -*- encoding utf-8 -*-
import arcpy
from XmlImportException import XmlImportException


class XmlWorkspaceImporter:

    def __init__(self, properties, connection_name):
        self.__base_path = properties["connection_file_path"]
        self.__sde_file = self.__base_path + "/config/" + connection_name + ".sde"
        self.__data = self.__base_path + "/buffer/"

    def set_console_logger(self, console_logger):
        self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        self.__f_logger = file_logger

    def archive(self, data_name):
        self.__c_logger.info("IMPORT PROPERTIES: \n"
                             + self.__sde_file + "\n"
                             + self.__data)
        self.__f_logger.info("IMPORT PROPERTIES: \n"
                             + self.__sde_file + "\n"
                             + self.__data)
        try:
            self.__c_logger.info("IMPORT SDE FILE FORM BUFFER")
            self.__f_logger.info("IMPORT SDE FILE FORM BUFFER")
            arcpy.ImportXMLWorkspaceDocument_management(
                self.__sde_file,
                self.__data + data_name,
                "DATA"
                )
        except Exception as e:
            self.__c_logger.exception("EXCEPTION WHILE IMPORTING SDE FILE FORM BUFFER: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE IMPORTING SDE FILE FORM BUFFER: " + str(e))
            raise XmlImportException("Exception while importing the xml file to the read only schema: " +
                                     str(e))
