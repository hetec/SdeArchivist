# -*- encoding utf-8 -*-
from xmlWorkspaceDocumentExportError import XMLWorkspaceDocumentExportError
import os
import arcpy
import RenamingException

class DatasetRenameService:
    """
    Service to rename a persisted dataset.

    """

    def __init__(self, archive_properties, existence_validator):
        """
        Create a new instance of the DatasetRenameService

        :param archive_properties: A map with the property data for the sde archive
        :param existence_validator: An existence validator instance
        :return: Name with counter (String)
        """
        self.__path = archive_properties["project_root"] + "/config/sdearchive.sde/"
        self.__validator = existence_validator

    def __check_existence_and_incr(self, name):
        counter = 1
        temp_name = name
        while self.__validator.imported_sde_data_exists("sdearchive", temp_name):
            temp_name = name + "_" + str(counter)
            counter += 1
        return temp_name

    def rename(self, data):
        """
        Renames a persisted dataset in the manner OLDUSER.datasetname -> NEWUSER.datasetname_OLDUSER.
        If the dataset name already exists a counter will be added like NEWUSER.datasetname_OLDUSER_Counter

        :param data: The name of the data without an extension -> USER.dataname
        :return: The new name
        :exception: Throws Renaming Exception
        """
        old_name = "SDE." + data.split(".")[1]
        self.__c_logger.debug("Old dataset name in sde archive: " + old_name)
        self.__f_logger.debug("Old dataset name in sde archive: " + old_name)
        new_name = old_name + "_" + data.split(".")[0]
        new_name = self.__check_existence_and_incr(new_name)

        self.__c_logger.debug("Try to rename to new dataset name: " + new_name)
        self.__f_logger.debug("Try to rename to new dataset name: " + new_name)

        try:
            arcpy.env.workspace = self.__path

            arcpy.Rename_management(
                old_name,
                new_name
            )
        except Exception as e:
            self.__c_logger.debug("There was an error during renaming the persisted data: " + str(e))
            self.__f_logger.debug("There was an error during renaming the persisted data: " + str(e))
            raise RenamingException.RenamingException(
                "There was an error during renaming the persisted data: " + str(e))

        return new_name

    def setConsoleLogger(self, consoleLogger):
        self.__c_logger = consoleLogger

    def setFileLogger(self, fileLogger):
        self.__f_logger = fileLogger
