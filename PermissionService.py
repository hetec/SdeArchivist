# -*- encoding utf-8 -*-
import arcpy


class PermissionService:
    """
    Changes the permissions of a user concerning a defined data set
    """

    def __init__(self, properties, connection_name):
        self.__base_path = properties["project_root"]
        self.__sde_file = self.__base_path + "/config/" + connection_name + ".sde"

    def set_console_logger(self, console_logger):
        self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        self.__f_logger = file_logger

    def grant_read_permission(self, user, data_set_name):
        """
        Grants the read permission for the data set to the user

        :param user: The user who gets the permission
        :param data_set_name: The data set for which the permission is granted
        :exception: Exception
        """
        try:
            data_set = self.__sde_file + "/" + str(data_set_name)
            arcpy.ChangePrivileges_management (data_set, str(user), "GRANT")
        except Exception as e:
            self.__c_logger.exception("Exception while granting permission to: " + str(user) + ": " + str(e))
            self.__f_logger.exception("Exception while granting permission to: " + str(user) + ": " + str(e))
            raise Exception("Exception while granting permission to: " + str(user) + ": " + str(e))
