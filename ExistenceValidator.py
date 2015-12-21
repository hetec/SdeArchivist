# -*- encoding utf-8 -*-
import os
import arcpy
from ExistenceException import ExistenceException


class ExistenceValidator():
    """
    Verifies the existence of files
    """

    def __init__(self,):
        pass

    def set_console_logger(self, console_logger):
            self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        self.__f_logger = file_logger

    def directory_exists(self, dir):
        path = os.path.abspath(dir)
        self.__c_logger.debug("Dir exists: " + str(os.path.exists(path)))
        self.__f_logger.debug("Dir exists: " + str(os.path.exists(path)))
        return os.path.exists(path)

    def buffered_xml_exists(self, file_name):
        """
        Checks if a given file exists in the buffer folder
        :param file_name: The file to verify (String)
        :return: (Boolean)
        """
        path = os.path.join(os.path.abspath("buffer"), file_name)
        self.__c_logger.debug("XML exists: " + str(os.path.exists(path)))
        self.__f_logger.debug("XML exists: " + str(os.path.exists(path)))
        return os.path.exists(path)

    def config_file_exists(self, file_name):
        """
        Checks if a given file exists in the config folder
        :param file_name: The file to verify (String)
        :return: (Boolean)
        """
        path = os.path.join(os.path.abspath("config"), file_name)
        self.__c_logger.debug("Config exists: " + str(os.path.exists(path)))
        self.__f_logger.debug("Config exists: " + str(os.path.exists(path)))
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
            self.__c_logger.debug("Dir exists: " + str(arcpy.Exists(file_name)))
            self.__f_logger.debug("Dir exists: " + str(arcpy.Exists(file_name)))
            return arcpy.Exists(file_name)
        else:
            raise ExistenceException("Missing connection file in the config folder")


if __name__ == "__main__":
    validator = ExistenceValidator()
    print(validator.imported_sde_data_exists("sde", "SDE.alles"))

