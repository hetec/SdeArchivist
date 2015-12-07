# -*- encoding utf-8 -*-
import io
import json
import RequiredTag

class SdeArchivistProperties:

    def __init__(self, ref):
        self.__config = ""
        self.__ref = ref
        self.tag_config = {}
        self.database_config = {}
        self.__read_config()

    def __read_config(self):
        try:
            config_stream = io.open(file="config/archivist_config.json", encoding="utf-8")
            self.__config = json.loads(config_stream.read())
            self.tag_config = self.__extract_tag_config(self.__config)
            self.database_config = self.__extract_db_config(self.__config)
        finally:
            config_stream.close()

    def __extract_tag_config(self, dct):
        if "tag_config" in dct:
            return [RequiredTag.RequiredTag(entry["tag_name"], entry["is_empty"] if "is_empty" in entry else False)
                    for entry in dct["tag_config"]["required"]]

    def __extract_db_config(self, dct):
        if "database_config" in dct:
            if self.__validate_db_config(dct["database_config"]):
                return dct["database_config"]
            else:
                raise ValueError("Missing database config entry (url, port, service, username, password)")

    def __validate_db_config(self,config):
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
        return valid_config

if __name__ == "__main__":
    props = SdeArchivistProperties("config/archivist_config.json")
    for tag in props.tag_config:
        print tag.tag_name()
        print tag.is_empty()