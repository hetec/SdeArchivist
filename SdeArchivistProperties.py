# -*- encoding utf-8 -*-
import io
import json
import RequiredTag


class SdeArchivistProperties:
    def __init__(self, ref):
        """
        Creates a new SdeArchivistProperties instance containing the config data

        Properties:
            tag_config (Dictionary)
            database_config (Dictionary)
            ldap_config (Dictionary)
            mail_config (Dictionary)
            sde_config (Dictionary)

        :param ref: The location of the 'archivist_config.json' configuration file
        :return: new SdeArchivistProperties instance
        """
        self.__config = ""
        self.__ref = ref
        self.tag_config = {}
        self.database_config = {}
        self.ldap_config = {}
        self.mail_config = {}
        self.sde_config = {}
        self.sdearchive_config = {}
        self.__read_config()

    def __read_config(self):
        try:
            config_stream = io.open(file="config/archivist_config.json", encoding="utf-8")
            self.__config = json.loads(config_stream.read())
            self.tag_config = self.__extract_tag_config(self.__config)
            self.database_config = self.__extract_db_config(self.__config)
            self.ldap_config = self.__extract_ldap_config(self.__config)
            self.mail_config = self.__extract_mail_config(self.__config)
            self.sde_config = self.__extract_sde_config(self.__config)
            self.sdearchive_config = self.__extract_sdearchive_config(self.__config)
        finally:
            config_stream.close()

    def __extract_tag_config(self, dct):
        if "tag_config" in dct:
            return {str(entry["tag_name"]): RequiredTag.RequiredTag(
                entry["tag_name"],
                entry["is_empty"] if "is_empty" in entry else False,
                entry["attributes"] if "attributes" in entry else [])
                    for entry in dct["tag_config"]["required"]}

    def __extract_db_config(self, dct):
        if "database_config" in dct:
            if self.__validate_db_config(dct["database_config"]):
                return dct["database_config"]
            else:
                raise ValueError("Missing database config entry (url, port, service, username, password)")

    def __extract_ldap_config(self, dct):
        if "ldap_config" in dct:
            if self.__validate_ldap_config(dct["ldap_config"]):
                return dct["ldap_config"]
            else:
                raise ValueError("Missing ldap config entry (server, dn)")

    def __extract_mail_config(self, dct):
        if "mail_config" in dct:
            if self.__validate_mail_config(dct["mail_config"]):
                return dct["mail_config"]
            else:
                raise ValueError("Missing mail config entry "
                                 "(smtp_server, port, from, subject, password, failure_text, additional_recipients)")

    def __extract_sde_config(self, dct):
        if "sde_config" in dct:
            if self.__validate_sde_config(dct["sde_config"]):
                return dct["sde_config"]
            else:
                raise ValueError("Missing sde config entry "
                                 "(connectionFilePath, database_type, instance_name, auth_method, username, password)")

    def __extract_sdearchive_config(self, dct):
        if "sdearchive_config" in dct:
            if self.__validate_sdearchive_config(dct["sdearchive_config"]):
                return dct["sdearchive_config"]
            else:
                raise ValueError("Missing sdearchive config entry "
                                 "(connectionFilePath, database_type, instance_name, auth_method, username, password)")

    def __validate_db_config(self, config):
        valid_config = True
        if "url" not in config:
            valid_config = False
        if "port" not in config:
            valid_config = False
        if "service" not in config:
            valid_config = False
        if "username" not in config:
            valid_config = False
        if "password" not in config:
            valid_config = False
        if "request_table" not in config:
            valid_config = False
        if "content_table" not in config:
            valid_config = False
        return valid_config

    def __validate_mail_config(self, config):
        valid_config = True
        if "smtp_server" not in config:
            valid_config = False
        if "port" not in config:
            valid_config = False
        if "from" not in config:
            valid_config = False
        if "subject" not in config:
            valid_config = False
        if "password" not in config:
            valid_config = False
        if "username" not in config:
            valid_config = False
        if "failure_message" not in config:
            valid_config = False
        if "additional_recipients" not in config:
            valid_config = False
        return valid_config

    def __validate_sde_config(self, config):
        valid_config = True
        if "connection_file_path" not in config:
            valid_config = False
        if "database_type" not in config:
            valid_config = False
        if "instance_name" not in config:
            valid_config = False
        if "auth_method" not in config:
            valid_config = False
        if "username" not in config:
            valid_config = False
        if "password" not in config:
            valid_config = False
        return valid_config

    def __validate_sdearchive_config(self, config):
        valid_config = True
        if "connection_file_path" not in config:
            valid_config = False
        if "database_type" not in config:
            valid_config = False
        if "instance_name" not in config:
            valid_config = False
        if "auth_method" not in config:
            valid_config = False
        if "username" not in config:
            valid_config = False
        if "password" not in config:
            valid_config = False
        return valid_config

    def __validate_ldap_config(self, config):
        valid_config = True
        if "server" not in config:
            valid_config = False
        if "dn" not in config:
            valid_config = False
        return valid_config


if __name__ == "__main__":
    props = SdeArchivistProperties("config/archivist_config.json")
    for tag in props.database_config:
        print tag
        print props.database_config[tag]
