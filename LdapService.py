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
        :raises: Exception if an error occurs while connecting to ldap
        """
        self.__props = properties
        try:
            self.__ldapObj = ldap.initialize("ldap://" + self.__props["server"])
        except Exception as e:
            raise Exception("Not able to connect to " + self.__props["server"] + ": " + str(e.message))

    def get_email_by_uid(self, uid):
        """
        Finds a email address by a given uid
        :param uid: The ldap name of the user (String)
        :return: Email (String)
        :raises: Exception if an error occurs while connecting to ldap
        """
        try:
            res = self.__ldapObj.search_s(self.__props["dn"],ldap.SCOPE_SUBTREE,"uid=" + uid)
        except Exception as e:
            raise Exception("Not able to execute the search request on the server: '" + self.__props["server"]
                            + "', ERROR: " + str(e.message))
        if len(res) > 0 and res is not None:
            email = res[0][1]["mail"][0]
        else:
            raise Exception("No ldap entry for '" + uid + "'")
        return email



