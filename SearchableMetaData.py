# -*- encoding utf-8 -*-
import json

class BunchDict(dict):
    """
    Data container class to hold dynamic meta data
    """
    def __init__(self,**kw):
        dict.__init__(self,kw)
        self.__dict__.update(kw)

class SearchableMetaData:
    """
    Collects the meta data and returns them as json
    """
    def __init__(self, name, meta_data):
        self.__to_json = BunchDict(name=name, meta_data=meta_data)

    def addEntry(self, **entry):
        """
        Add a new entry to the data object

        :param entry: The data you want to add (Arbitrary)
        """
        self.__to_json.update(entry)

    def get_json(self):
        """
        Get the json representation of the current object

        :return: (String)
        """
        return json.dumps(self.__to_json)
