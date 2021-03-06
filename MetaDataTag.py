# -*- encoding utf-8 -*-
import copy


class MetaDataTag:
    """
    Represents a tag in the xml meta data
    """

    def __init__(self, key, tag_name, is_empty=False, optional=False, mapped_name="", attributes=()):
        """
        Creates a new MetaDataTag object

        :param key: A unique identifier
        :param tag_name: The name of the tag (String)
        :param attributes: The required attributes of this tag (List)
        :param mapped_name: If populated this name is used instead of the xml tag name (String)
        :param is_empty: Defines if a tag has content or not (Boolean, Default: False)
        :return: New MetaDataTag object
        """
        self.__key = key
        self.__tag_name = tag_name
        self.__mapped_name = mapped_name
        self.__attributes = attributes
        self.__is_empty_tag = is_empty
        self.__optional = optional

    def tag_key(self):
        """
        Returns the defined key of the Tag

        :return: Tag key (String)
        """
        return self.__key


    def tag_name(self):
        """
        Returns the defined name of the Tag

        :return: Tag name (String)
        """
        return self.__tag_name

    def mapped_name(self):
        """
        Returns the value for the mapped name

        :return: mapped_name (String)
        """
        return self.__mapped_name

    def is_empty(self):
        """
        Returns if the tag may be empty

        :return: True if the tag is empty else False (Boolean)
        """
        return self.__is_empty_tag

    def is_optional(self):
        """
        Returns if the tag is optional

        :return: True if the tag is optional else False (Boolean)
        """
        return self.__optional

    def attributes(self):
        """
        Returns a copy of the attributes

        :return: (List)
        """
        return copy.copy(self.__attributes)
