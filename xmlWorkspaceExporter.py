
from xmlWorkspaceDocumentExportError import XMLWorkspaceDocumentExportError
import os
import arcpy


class XmlWorkspaceExporter:
    """
    Exports the specified SDE data to an xml file
    """

    def __init__(self, properties):
        """
        Creates a new XmlWorkspaceExporter instance
        :param properties: Properties which must provide the 'connection_file_path'
        :return: new XmlWorkspaceExporter instance
        """
        self.__base_path = properties["connection_file_path"]

    def export(self, data):
        """
        Exports the assigned data as an xmlWorkspaceDocument

        - Includes the data and the meta data if existing
        :param data: The name of the SDE DataSet. Must be exportable as xmlWorkspaceDocument (String)
        :return:
        """
        input_file = self.__base_path + "/config/connection.sde"
        location = self.__base_path + "/buffer"
        input_file = input_file + "/" + data
        data = data.strip(" \t")
        output_file = location + "/" + data.encode('ascii', 'ignore') + ".xml"
        output_file = self.__check_file_name(output_file, data.encode('ascii', 'ignore'))
        print "---------XMLExporter---------"
        print "INPUT: " + input_file
        print "OUTPUT: " + output_file
        try:
            arcpy.ExportXMLWorkspaceDocument_management(input_file,
                                                        output_file,
                                                        "DATA",
                                                        "BINARY",
                                                        "METADATA")
            print "\nExport to xml file -> " + data.encode('ascii', 'ignore') + " is finished!"
        except arcpy.ExecuteError as e:
            raise XMLWorkspaceDocumentExportError("Error while creating XMLWorkspaceDocument: " + e.message)

    def __check_file_name(self, output, identity):
        counter = 0
        while os.path.isfile(output):
            counter += 1
            output = self.__base_path + "/buffer/" + identity + "_copy" + str(counter) + ".xml"
        return output
