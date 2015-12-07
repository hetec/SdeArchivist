import ldap
import ldif
import sys


class LdapService:

    def __init__(self):
        self.__ldapObj = ldap.initialize("ldap://ldap.intranet.ufz.de")

    def get_email_by_uid(self, uid):
        res = self.__ldapObj.search_s("ou=people,dc=ufz,dc=de",ldap.SCOPE_SUBTREE,"uid=" + uid)
        email = res[0][1]["mail"][0]
        return email



