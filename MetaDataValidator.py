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
        :raises: Exception if a tag is missing
        :raises: Exception if a tag has no content, however it's defined to have one
        """
        found_tags = self.__find_all_xml_tags(self.__required_tags)
        self.__validate_tag(found_tags, meta_data)

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

    def __validate_existence(self, tag, found_tags):
        if str(tag.tag_name()) not in found_tags:
            return tag.tag_name(), "MISSING"
        else:
            return tag.tag_name(), "OK"

    def __validate_not_empty(self, required_tag, found_tags):
        if not required_tag.is_empty() and required_tag.tag_name() in found_tags:
            if not (False if (found_tags[required_tag.tag_name()].text is None)
                    else len(found_tags[required_tag.tag_name()].text)) > 0:
                return required_tag.tag_name(), "CONTENT EXPECTED"
        elif required_tag.is_empty() and required_tag.tag_name() in found_tags:
            print "Checking empty tag: " + required_tag.tag_name()
            if not self.__validate_attribute("value", found_tags[required_tag.tag_name()]):
                return required_tag.tag_name(), "No attribute 'value'"
        return required_tag.tag_name(), "OK"

    def __validate_attribute(self, attr_name, tag_name):
        attributes = tag_name.attrib
        for a in attributes:
            print a + "-->" + attributes[a]
        if attr_name in attributes and len(attributes[a]) > 0:
            return True
        else:
            return False

    def __find_xml_tag(self, tag_name):
        root = etree.fromstring(self.__xml)
        print "ROOT:"
        tag_instances = root.findall(".//" + tag_name)
        return tag_instances

    def __find_all_xml_tags(self, tags):
        tag_buffer = []
        for tag in tags:
            tag_buffer.extend(self.__find_xml_tag(tag.tag_name()))
        return {tag.tag: tag for tag in tag_buffer}
