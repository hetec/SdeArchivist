# -*- encoding utf-8 -*-
import copy
import json
import types

class MetaData:
    """
    Represents the meta data of a SDE entry
    """
    def __init__(self):
        self.__is_valid = True
        self.__meta_data_info = {}
        self.__meta_data = {}

    def add_meta_data_info(self, name, value):
        """
        Adds a meta date as key value pair

        :param name: The name of the meta date (String)
        :param value: The value of the meta date (String)
        """
        self.__meta_data_info[name] = value

    def add_meta_data(self, name, value):
        """
        Adds a meta date as key value pair

        :param name: The name of the meta date (String)
        :param value: The value of the meta date (String)
        """
        #name = self.__replace_existing_key_names(name)
        self.__meta_data[name] = self.__handle_duplicates(name, value)

    def meta_data_info(self):
        """
        Returns a defensive copy of the contained meta data as dictionary {name:state}

        :return: dictionary with meta data
        """
        return copy.copy(self.__meta_data_info)

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
        """
        self.__is_valid = value

    def is_valid(self):
        """
        Shows if the meta data are valid

        :return: If the meta data are valid (Boolean)
        """
        return self.__is_valid

    def __replace_existing_key_names(self, name):
        temp_name = name
        counter = 1
        while str(temp_name) in self.meta_data():
            temp_name = name + "_" + str(counter)
            counter += 1
        return temp_name

    def __handle_duplicates(self, name, value):
        element_list = None
        if name in self.__meta_data and type(self.__meta_data[name]) == types.ListType:
            element_list = self.__meta_data[name]
            element_list.append(str(value))
            return element_list
        elif str(name) in self.meta_data():
            current_value = self.__meta_data[name]
            element_list = [str(current_value), str(value)]
            return element_list
        else:
            return str(value)
