import ldap
import ldif
import sys


class LdapService:

    def __init__(self, properties):
        self.__props = properties
        self.__ldapObj = ldap.initialize("ldap://" + self.__props["server"])

    def get_email_by_uid(self, uid):
        res = self.__ldapObj.search_s(self.__props["dn"],ldap.SCOPE_SUBTREE,"uid=" + uid)
        email = res[0][1]["mail"][0]
        return email



