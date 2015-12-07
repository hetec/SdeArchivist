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
        """
        self.__props = properties
        self.__ldapObj = ldap.initialize("ldap://" + self.__props["server"])

    def get_email_by_uid(self, uid):
        """
        Finds a email address by a given uid
        :param uid: The ldap name of the user (String)
        :return: Email (String)
        """
        res = self.__ldapObj.search_s(self.__props["dn"],ldap.SCOPE_SUBTREE,"uid=" + uid)
        email = res[0][1]["mail"][0]
        return email



