# -*- encoding utf-8 -*-
import copy


class MetaData:
    """
    Represents the meta data of a SDE entry
    """
    def __init__(self):
        self.__is_valid = True
        self.__meta_data = {}

    def add_meta_data(self, name, value):
        """
        Adds a meta date as key value pair

        :param name: The name of the meta date (String)
        :param value: The value of the meta date (String)
        :return: void
        """
        self.__meta_data[name] = value

    def meta_data(self):
        """
        Returns a defensive copy of the contained meta data as dictionary {name:state}

        :return: dictionary with meta data
        """
        return copy.copy(self.__meta_data)

    def set_valid(self, value):
        """
        Declares the related meta data set as valid (or not)
        :param value: Value to mark the meta data as valid (Boolean, Default: False)
        :return: void
        """
        self.__is_valid = value

    def is_valid(self):
        """
        Shows if the meta data are valid

        :return: If the meta data are valid (Boolean)
        """
        return self.__is_valid


if __name__ == "__main__":
    meta = MetaData()
    meta.add_meta_data("eins","1")
    meta.add_meta_data("zwei","2")
    print(meta.meta_data())
    meta1 = meta.meta_data()
    print(meta1)
    meta1["eins"] = "99999"
    print(meta1)
    print(meta.meta_data())