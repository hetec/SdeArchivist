# -*- encoding utf-8 -*-


class RequiredTag:
    """
    Represents a tag which is required by valid meta data
    """

    def __init__(self, tag_name, is_empty=False):
        """
        Creates a new RequiredTag object

        :param tag_name: The name of the tag (String)
        :param is_empty: Defines if a tag has content or not (Boolean, Default: False)
        :return: New RequiredTag object
        """
        self.__tag_name = tag_name
        self.__is_empty_tag = is_empty

    def tag_name(self):
        """
        Returns the defined name of the Tag

        :return: Tag name (String)
        """
        return self.__tag_name

    def is_empty(self):
        """
        Returns if the tag may be empty

        :return: True if the tag is empty else False (Boolean)
        """
        return self.__is_empty_tag
