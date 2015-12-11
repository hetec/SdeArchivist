# -*- encoding utf-8 -*-
import arcpy


class XmlWorkspaceImporter:

    def __init__(self, properties):
        self.__base_path = properties["connection_file_path"]
        self.__sde_file = self.__base_path + "/config/connection.sde"
        self.__data = self.__base_path + "/buffer/"

    def archive(self, data_name):
        arcpy.ImportXMLWorkspaceDocument_management(
            self.__sde_file,
            self.__data + data_name,
            "DATA"
            )
