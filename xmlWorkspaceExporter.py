# -*- encoding utf-8 -*-
from xmlWorkspaceDocumentExportError import XMLWorkspaceDocumentExportError
import os
import arcpy


class XmlWorkspaceExporter:
    """
    Exports the specified SDE data to an xml file
    """

    def __init__(self, properties, connection_name):
        """
        Creates a new XmlWorkspaceExporter instance

        :param properties: Properties which must provide the 'project_root' (Map)
        :param connection_name: Name of the connection (String)
        """
        self.__base_path = properties["project_root"]
        self.__connection_name = connection_name

    def set_console_logger(self, console_logger):
            self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        self.__f_logger = file_logger

    def export(self, data):
        """
        Exports the assigned data as an xmlWorkspaceDocument

        - Includes the data and the meta data if existing

        :param data: The name of the SDE DataSet. Must be exportable as xmlWorkspaceDocument (String)
        """
        self.__c_logger.info("EXPORTIERE: " + str(data))
        self.__f_logger.info("EXPORTIERE: " + str(data))

        input_file = self.__base_path + "/config/" + self.__connection_name + ".sde"

        location = self.__base_path + "/buffer"

        input_file = input_file + "/" + data
        self.__c_logger.info("INPUT FILE: " + input_file)
        self.__f_logger.info("INPUT FILE: " + input_file)

        data = data.strip(" \t")

        output_file = location + "/" + data.encode('ascii', 'ignore') + ".xml"

        output_file = self.__check_file_name(output_file, data.encode('ascii', 'ignore'))
        self.__c_logger.info("OUTPUT FILE: " + output_file)
        self.__f_logger.info("OUTPUT FILE: " + output_file)

        try:
            arcpy.ExportXMLWorkspaceDocument_management(input_file,
                                                        output_file,
                                                        "DATA",
                                                        "BINARY",
                                                        "METADATA")
        except arcpy.ExecuteError as e:
            self.__c_logger.exception("EXCEPTION WHILE EXPORTING: " + str(e))
            self.__f_logger.exception("EXCEPTION WHILE EXPORTING: " + str(e))
            raise XMLWorkspaceDocumentExportError("Error while creating XMLWorkspaceDocument: " + e.message)

    def __check_file_name(self, output, identity):
        counter = 0
        while os.path.isfile(output):
            counter += 1
            output = self.__base_path + "/buffer/" + identity + "_copy" + str(counter) + ".xml"
        return output
