# -*- encoding utf-8 -*-
import ldap


class LdapService:
    """
    Connects to the defined ldap server
    """

    def __init__(self, properties):
        """
        Creates a LdapSever instance

        :param properties: Properties to connect to the ldap server (Dictionary)
        :return: New LdapService object
        :exception: Exception if an error occurs while connecting to ldap
        """
        self.__props = properties
        try:
            self.__ldapObj = ldap.initialize("ldap://" + self.__props["server"])
        except Exception as e:
            raise Exception("Not able to connect to " + self.__props["server"] + ": " + str(e.message))

    def set_console_logger(self, console_logger):
        self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        self.__f_logger = file_logger

    def get_email_by_uid(self, uid):
        """
        Finds a email address by a given uid

        :param uid: The ldap name of the user (String)
        :return: Email (String)
        :exception: Exception if an error occurs while connecting to ldap
        """
        try:
            res = self.__ldapObj.search_s(self.__props["dn"], ldap.SCOPE_SUBTREE, "uid=" + uid)
            self.__c_logger.debug("Get email address for " + uid)
            self.__f_logger.debug("Get email address for " + uid)
        except Exception as e:
            self.__c_logger.exception("EXCEPTION while getting email address for " + uid + ": " + res + ": " + str(e))
            self.__f_logger.exception("EXCEPTION while getting email address for " + uid + ": " + res + ": " + str(e))
            raise Exception("Not able to execute the search request on the server: '" + self.__props["server"] +
                            "', ERROR: " + str(e.message))
        if len(res) > 0 and res is not None:
            email = res[0][1]["mail"][0]
        else:
            self.__c_logger.exception("EXCEPTION while getting email address for " + uid + ": No ldap entry")
            self.__f_logger.exception("EXCEPTION while getting email address for " + uid + ": No ldap entry")
            raise Exception("No ldap entry for '" + uid + "'")
        return email



