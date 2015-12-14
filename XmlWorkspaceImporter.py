# -*- encoding utf-8 -*-
import arcpy
from XmlImportException import XmlImportException


class XmlWorkspaceImporter:

    def __init__(self, properties):
        self.__base_path = properties["connection_file_path"]
        self.__sde_file = self.__base_path + "/config/connection.sde"
        self.__data = self.__base_path + "/buffer/"

    def archive(self, data_name):
        try:
            arcpy.ImportXMLWorkspaceDocument_management(
                self.__sde_file,
                self.__data + data_name,
                "DATA"
                )
        except Exception as e:
            raise XmlImportException("Exception while importing the xml file to the read only schema: " +
                                     str(e))
