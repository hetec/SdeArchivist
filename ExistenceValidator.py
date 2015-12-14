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

    def buffered_xml_exists(self, file_name):
        """
        Checks if a given file exists in the buffer folder
        :param file_name: The file to verify (String)
        :return: (Boolean)
        """
        path = os.path.join(os.path.abspath("buffer"), file_name)
        return os.path.exists(path)

    def config_file_exists(self, file_name):
        """
        Checks if a given file exists in the config folder
        :param file_name: The file to verify (String)
        :return: (Boolean)
        """
        path = os.path.join(os.path.abspath("config"), file_name)
        return os.path.exists(path)

    def imported_sde_data_exists(self, file_name):
        """
        Checks if a given file exists in the sde database
        :param file_name: The file to verify (String)
        :return: (Boolean)
        """
        if self.config_file_exists("connection.sde"):
            path = os.path.abspath("config/connection.sde/")
            arcpy.env.workspace = path
            print(arcpy.Exists(file_name))
        else:
            raise ExistenceException("Missing connection file in the config folder")


if __name__ == "__main__":
    validator = ExistenceValidator()
    validator.imported_sde_data_exists("SDE.alles")

