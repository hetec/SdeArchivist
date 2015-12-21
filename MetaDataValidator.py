# -*- encoding utf-8 -*-
import xml.etree.ElementTree as etree


class MetaDataValidator:
    """
    Validates some meta data represented as xml

    The meta data contained in the xml tree are tested
    against a assigned set of required meta data
    """

    def __init__(self, xml, required_tags):
        """
        Creates a MetaDataValidator object

        :param xml: The data to check (XML as String)
        :param required_tags: The required meta data (List of MetaData objects)
        :return: New MetaDataValidator object
        """
        self.__xml = xml
        self.__required_tags = required_tags

    def set_console_logger(self, console_logger):
        self.__c_logger = console_logger

    def set_file_logger(self, file_logger):
        self.__f_logger = file_logger

    def validate(self, meta_data):
        """
        Starts the validation process on the data specified on the creation of the validator

        :param meta_data: The meta data container which gets filled during the validation.
        """
        self.__c_logger.info("START VALIDATION")
        self.__f_logger.info("START VALIDATION")
        for tag in self.__required_tags:
            self.__find_xml_tag(self.__required_tags[tag],meta_data)

        self.__c_logger.info("END VALIDATION")
        self.__f_logger.info("END VALIDATION")

    def __validate_attribute(self, attribute_names, tag_name):
        attributes = tag_name.attrib
        missing_attr = []
        if len(attribute_names) > 0:
            if len(attributes) > 0:
                for a in attribute_names:
                    if a in attributes:
                        if len(attributes[a]) <= 0:
                            missing_attr.append(a)
                    else:
                        missing_attr.append(a)
                if len(missing_attr) > 0:
                    result = "Missing attributes: "
                    for a in missing_attr:
                        result += str(a) + " "
                    self.__c_logger.info("MISSING ATTR - RESULT: " + result)
                    self.__f_logger.info("MISSING ATTR - RESULT: " + result)
                    return result
                else:
                    self.__c_logger.info("ATTR OK")
                    self.__f_logger.info("ATTR OK")
                    return ""
            else:
                result = "Missing attributes: "
                for a in attribute_names:
                    result += str(a) + " "
                self.__c_logger.info("MISSING ATTR - RESULT: " + result)
                self.__f_logger.info("MISSING ATTR - RESULT: " + result)
                return result
        else:
            self.__c_logger.info("NO ATTRS --> OK")
            self.__f_logger.info("NO ATTRS --> OK")
            return ""

    def __find_xml_tag(self, tag_name, meta_data):
        self.__c_logger.info("Fetch tags from the meta data xml")
        self.__f_logger.info("Fetch tags from the meta data xml")
        root = etree.fromstring(self.__xml)
        tag_instances = root.findall(".//" + tag_name.tag_name())
        if tag_instances:
            self.__c_logger.info("EXISTS: " + tag_name.tag_name() + " (" + len(tag_instances) + ")")
            self.__f_logger.info("EXISTS: " + tag_name.tag_name() + " (" + len(tag_instances) + ")")
            for tag in tag_instances:
                msg = self.__validate_not_empty(tag, tag_name)
                meta_data.add_meta_data(tag_name.tag_name(), msg)
                if msg is not "OK" and meta_data.is_valid() is True:
                    meta_data.set_valid(False)
        else:
            self.__c_logger.info("MISSING: " + tag_name.tag_name())
            self.__f_logger.info("MISSING: " + tag_name.tag_name())
            meta_data.add_meta_data(tag_name.tag_name(), "Missing")
            if meta_data.is_valid() is True:
                meta_data.set_valid(False)
        return tag_instances

    def __validate_not_empty(self, tag, tag_config):
        if not tag_config.is_empty():
            self.__c_logger.info("IS EMPTY IS NOT ALLOWED: " + tag_config.tag_name())
            self.__f_logger.info("IS EMPTY IS NOT ALLOWED: " + tag_config.tag_name())
            if not (False if (tag.text is None)
                    else len(tag.text)) > 0:
                self.__c_logger.info("NO CONTENT: " + tag_config.tag_name())
                self.__f_logger.info("NO CONTENT: " + tag_config.tag_name())
                return tag_config.tag_name(), "CONTENT EXPECTED"
            else:
                self.__c_logger.info("CHECK ATTR: " + tag_config.tag_name())
                self.__f_logger.info("CHECK ATTR: " + tag_config.tag_name())
                attr_check = self.__validate_attribute(tag_config.attributes(),tag)
                if len(attr_check) > 0:
                    return attr_check
        elif tag_config.is_empty():
            self.__c_logger.info("IS EMPTY IS ALLOWED: " + tag_config.tag_name())
            self.__f_logger.info("IS EMPTY IS ALLOWED: " + tag_config.tag_name())
            attr_check = self.__validate_attribute(tag_config.attributes(), tag)
            self.__c_logger.info("CHECK ATTR: " + tag_config.tag_name())
            self.__f_logger.info("CHECK ATTR: " + tag_config.tag_name())
            if len(attr_check) > 0:
                return attr_check
        return "OK"


