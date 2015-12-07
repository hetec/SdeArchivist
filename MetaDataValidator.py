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

    def validate(self):
        """
        Starts the validation process on the data specified on the creation of the validator

        :raises: Exception if a tag is missing
        :raises: Exception if a tag has no content, however it's defined to have one
        """
        found_tags = self.__find_all_xml_tags(self.__required_tags)
        self.__validate_tag(found_tags)

    def __validate_tag(self, found_tags):
        for tag in self.__required_tags:
            self.__validate_existence(tag, found_tags)
            self.__validate_not_empty(tag, found_tags)
        return True

    def __validate_existence(self, tag, found_tags):
        if str(tag.tag_name()) not in found_tags:
            raise Exception("Missing tag")

    def __validate_not_empty(self, required_tag, found_tags):
        if not required_tag.is_empty():
            if not (False if (found_tags[required_tag.tag_name()].text is None)
                    else len(found_tags[required_tag.tag_name()].text)) > 0:
                raise Exception("No content")

    def __find_xml_tag(self, tag_name):
        root = etree.fromstring(self.__xml)
        tag_instances = root.findall(".//" + tag_name)
        return tag_instances

    def __find_all_xml_tags(self, tags):
        tag_buffer = []
        for tag in tags:
            tag_buffer.extend(self.__find_xml_tag(tag.tag_name()))
        return {tag.tag: tag for tag in tag_buffer}
