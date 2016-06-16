# -*- encoding utf-8 -*-
import io
import json
import MetaDataTag
import logging


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

        :param ref: The location of the 'archivist_config.json' configuration file (String)
        :return: new SdeArchivistProperties instance
        """
        self.__config = ""
        self.__ref = ref
        self.tag_config = {}
        self.database_config = {}
        self.archive_database_config = {}
        self.ldap_config = {}
        self.mail_config = {}
        self.sde_config = {}
        self.sdearchive_config = {}
        self.log_config = {}
        self.elasticsearch_config = {}
        self.__read_config(ref)

    def __read_config(self, ref):
        try:
            config_stream = io.open(file=ref, encoding="utf-8")
            self.__config = json.loads(config_stream.read())
            self.tag_config = self.__extract_tag_config(self.__config)
            self.database_config = self.__extract_db_config(self.__config)
            self.archive_database_config = self.__extract_archive_db_config(self.__config)
            self.ldap_config = self.__extract_ldap_config(self.__config)
            self.mail_config = self.__extract_mail_config(self.__config)
            self.sde_config = self.__extract_sde_config(self.__config)
            self.sdearchive_config = self.__extract_sdearchive_config(self.__config)
            self.log_config = self.__extract_log_config(self.__config)
            self.elasticsearch_config = self.__extract_elasitcsearch_config(self.__config)
        finally:
            config_stream.close()

    def __extract_tag_config(self, dct):
        new_dict = {}
        for entry in dct["tag_config"]["tags"]:
            if self.__validate_reqired_tag_config(entry):
                new_dict[str(entry["tag_name"])] = MetaDataTag.MetaDataTag(
                    entry["key"],
                    entry["tag_name"],
                    entry["is_empty"] if "is_empty" in entry else False,
                    entry["optional"] if "optional" in entry else False,
                    entry["mapped_name"] if "mapped_name" in entry else entry["tag_name"],
                    entry["attributes"] if "attributes" in entry else [])
            else:
                raise ValueError("Missing tag_name for required tag config entry")
        return new_dict

    def __extract_db_config(self, dct):
        if "database_config" in dct:
            if self.__validate_db_config(dct["database_config"]):
                return dct["database_config"]
            else:
                raise ValueError("Missing database config entry "
                                 "(url, port, service, username, password, request_table, content_table)")

    def __extract_archive_db_config(self, dct):
        if "archive_database_config" in dct:
            if self.__validate_archive_db_config(dct["archive_database_config"]):
                return dct["archive_database_config"]
            else:
                raise ValueError("Missing archive database config entry "
                                 "(url, port, service, username, password, meta_data_table,"
                                 " export_meta_data_to_database)")

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
                                 "(smtp_server, port, from, subject, get_user_process_info,"
                                 " password, failure_subject, success_subject,"
                                 " default_message, admin_recipients,"
                                 "send_mails_to_user)")

    def __extract_sde_config(self, dct):
        if "sde_config" in dct:
            if self.__validate_sde_config(dct["sde_config"]):
                return dct["sde_config"]
            else:
                raise ValueError("Missing sde config entry "
                                 "(project_root, database_type, instance_name, auth_method, username, password)")

    def __extract_sdearchive_config(self, dct):
        if "sdearchive_config" in dct:
            if self.__validate_sdearchive_config(dct["sdearchive_config"]):
                return dct["sdearchive_config"]
            else:
                raise ValueError("Missing sdearchive config entry "
                                 "(project_root, database_type, instance_name, auth_method, username, password)")

    def __extract_log_config(self, dct):
        if "log_config" in dct:
            if self.__validate_log_config(dct["log_config"]):
                self.__check_log_level(dct["log_config"])
                return dct["log_config"]
            else:
                raise ValueError("Missing log config entry "
                                 "(level, file, log_file_size (bytes), log_file_count (int))")

    def __extract_elasitcsearch_config(self, dct):
        if "elasticsearch_config" in dct:
            if self.__validate_elasticsearch_config(dct["elasticsearch_config"]):
                return dct["elasticsearch_config"]
            else:
                raise ValueError("Missing log config entry "
                                 "(host, index, type, activated")

    def __validate_reqired_tag_config(self, config):
        valid_config = True
        if "tag_name" not in config:
            valid_config = False
        if "key" not in config:
            valid_config = False
        return valid_config

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

    def __validate_archive_db_config(self, config):
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
        if "meta_data_table" not in config:
            valid_config = False
        if "export_meta_data_to_database" not in config:
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
        if "get_user_process_info" not in config:
            valid_config = False
        if "password" not in config:
            valid_config = False
        if "username" not in config:
            valid_config = False
        if "default_message" not in config:
            valid_config = False
        if "failure_subject" not in config:
            valid_config = False
        if "success_subject" not in config:
            valid_config = False
        if "admin_recipients" not in config:
            valid_config = False
        if "send_mails_to_user" not in config:
            valid_config = False
        return valid_config

    def __validate_sde_config(self, config):
        valid_config = True
        if "project_root" not in config:
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
        if "project_root" not in config:
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

    def __validate_log_config(self, config):
        valid_config = True
        if "level" not in config:
            valid_config = False
        if "file" not in config:
            valid_config = False
        if "log_file_size" not in config:
            valid_config = False
        if "log_file_count" not in config:
            valid_config = False
        return valid_config

    def __check_log_level(self, config):
        l = str(config["level"]).lower()
        if l == "debug":
            config["level"] = logging.DEBUG
        elif l == "info":
            config["level"] = logging.INFO
        elif l == "warn":
            config["level"] = logging.WARNING
        elif l == "error":
            config["level"] = logging.ERROR
        elif l == "fatal":
            config["level"] = logging.FATAL
        else:
            raise ValueError("No valid log level! Try debug, info, warn, error or fatal")

    def __validate_elasticsearch_config(self, config):
        valid_config = True
        if "host" not in config:
            valid_config = False
        if "index" not in config:
            valid_config = False
        if "type" not in config:
            valid_config = False
        if "activated" not in config:
            valid_config = False
        return valid_config

if __name__ == "__main__":
    props = SdeArchivistProperties("config/archivist_config.json")
    for tag in props.database_config:
        print tag
        print props.database_config[tag]
