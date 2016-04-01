# -*- encoding utf-8 -*-
import os
import arcpy
from ExistenceException import ExistenceException


class ExistenceValidator:
    """
    Verifies the existence of files and directories
    """

    def __init__(self,):
        pass

    def set_console_logger(self, console_logger):
            self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        self.__f_logger = file_logger

    def directory_exists(self, dir):
        """
        Checks if a given directory exists

        :param dir: The directory name
        :return: (Boolean)
        """
        path = os.path.abspath(dir)
        self.__c_logger.debug(str(dir) + " exists: " + str(os.path.exists(path)))
        self.__f_logger.debug(str(dir) + " exists: " + str(os.path.exists(path)))
        return os.path.exists(path)

    def buffered_xml_exists(self, file_name):
        """
        Checks if a given file exists in the buffer folder

        :param file_name: The file to verify (String)
        :return: (Boolean)
        """
        path = os.path.join(os.path.abspath("buffer"), file_name)
        self.__c_logger.debug("Bufferd " + str(file_name) + " exists: " + str(os.path.exists(path)))
        self.__f_logger.debug("Bufferd " + str(file_name) + " exists: " + str(os.path.exists(path)))
        return os.path.exists(path)

    def config_file_exists(self, file_name):
        """
        Checks if a given file exists in the config folder

        :param file_name: The file to verify (String)
        :return: (Boolean)
        """
        path = os.path.join(os.path.abspath("config"), file_name)
        self.__c_logger.debug(str(file_name) + " exists: " + str(os.path.exists(path)))
        self.__f_logger.debug(str(file_name) + " exists: " + str(os.path.exists(path)))
        return os.path.exists(path)

    def imported_sde_data_exists(self, connection_name, file_name):
        """
        Checks if a given file exists in the sde database

        :param file_name: The file to verify (String)
        :return: (Boolean)
        """
        if self.config_file_exists(connection_name + ".sde"):
            path = os.path.abspath("config/" + connection_name + ".sde/")
            arcpy.env.workspace = path
            self.__c_logger.debug(str(connection_name) + ".sde" + " exists: " + str(arcpy.Exists(file_name)))
            self.__f_logger.debug(str(connection_name) + ".sde" + " exists: " + str(arcpy.Exists(file_name)))
            return arcpy.Exists(file_name)
        else:
            self.__c_logger.exception("EXCEPTION while checking the excistence of " + connection_name
                                      + "Missing connection file in the config folder")
            self.__f_logger.exception("EXCEPTION while checking the excistence of " + connection_name
                                      + "Missing connection file in the config folder")
            raise ExistenceException("Missing connection file in the config folder")

