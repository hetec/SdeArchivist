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

    def validate(self, meta_data):
        """
        Starts the validation process on the data specified on the creation of the validator

        :param meta_data: The meta data container which gets filled during the validation.
        """

        for tag in self.__required_tags:
            self.__find_xml_tag(self.__required_tags[tag],meta_data)

    def __validate_tag(self, found_tags, meta_data):
        for tag in self.__required_tags:
            exists = self.__validate_existence(tag, found_tags)
            if exists is not None:
                meta_data.add_meta_data(exists[0], exists[1])
                if exists[1] == "MISSING" and meta_data.is_valid() is True:
                    meta_data.set_valid(False)
            has_content = self.__validate_not_empty(tag, found_tags)
            if has_content is not None:
                if has_content[1] is not "OK" and meta_data.is_valid() is True:
                    meta_data.set_valid(False)
                meta_data.add_meta_data(has_content[0], has_content[1])
        return True

    def __validate_attribute(self, attribute_names, tag_name):
        attributes = tag_name.attrib
        missing_attr = []
        if len(attribute_names) > 0:
            if len(attributes) > 0:
                for a in attribute_names:
                    if a in attributes:
                        if len(attributes[a]) > 0:
                            missing_attr.append(a)
                    else:
                        missing_attr.append(a)
                if len(missing_attr) > 0:
                    result = "Missing attributes: "
                    for a in missing_attr:
                        result += str(a) + " "
                    print "Result: " + result
                    return result
                else:
                    return ""
            else:
                result = "Missing attributes: "
                for a in attribute_names:
                    result += str(a) + " "
                    print "Result: " + result
                return result
        else:
            return ""

    def __find_xml_tag(self, tag_name, meta_data):
        root = etree.fromstring(self.__xml)
        tag_instances = root.findall(".//" + tag_name.tag_name())
        if tag_instances:
            for tag in tag_instances:
                msg = self.__validate_not_empty(tag, tag_name)
                meta_data.add_meta_data(tag_name.tag_name(), msg)
        else:
            meta_data.add_meta_data(tag_name.tag_name(), "Missing")
            if meta_data.is_valid() is True:
                meta_data.set_valid(False)
        return tag_instances

    def __validate_not_empty(self, tag, tag_config):
        if not tag_config.is_empty():
            if not (False if (tag.text is None)
                    else len(tag.text)) > 0:
                return tag_config.tag_name(), "CONTENT EXPECTED"
            else:
                attr_check = self.__validate_attribute(tag_config.attributes(),tag)
                if len(attr_check) > 0:
                    return attr_check
        elif tag_config.is_empty():
            attr_check = self.__validate_attribute(tag_config.attributes(), tag)
            if len(attr_check) > 0:
                return attr_check
        return "OK"


