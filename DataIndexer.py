from urllib import urlencode
import httplib2
import SearchableMetaData
from IndexingException import IndexingException
from FailedIndexingCache import FailedIndexingCache

class DataIndexer:
    """
    Enables the indexing of meta data as json
    """

    def __init__(self, config):
        """
        Create a new preconfigured instance

        :param config: The elasticsearch_config (Map)
        """
        self.__config = config

    def set_console_logger(self, instance):
        self.__c_logger = instance

    def set_file_logger(self, instance):
        self.__f_logger = instance

    def index(self, name, meta_data):
        """
        Indexes the given name and the meta data into elasticsearch.
        Uses or creates the index and type defined in the config

        :param name: Name of the sdearchive dataset (String)
        :param meta_data: Set of meta data (Map)
        :exception: Throws an IndexingException if something went wrong during the request
        """

        data = "No Data"
        try:
            data = SearchableMetaData.SearchableMetaData(name, meta_data.meta_data()).get_json()
            self.__c_logger.debug("Indexing data: " + str(data))
            self.__f_logger.debug("Indexing data: " + str(data))
            httplib2.debuglevel = 1
            h = httplib2.Http('.cache')
            url = self.__config["host"] + "/" + self.__config["index"] + "/" + self.__config["type"]
            print "DATA->" + data
            print "URL->" + url
            resp, content = h.request(url,
                                      "POST",
                                      data
                                      )
        except Exception as e:
            cache = FailedIndexingCache()
            cache.write_to_cache(data)

            self.__c_logger.exception("ERROR while indexing data: " + str(data) + "\n\n" + e.message)
            self.__f_logger.exception("ERROR while indexing data: " + str(data) + "\n\n" + e.message)
            raise IndexingException("ERROR while indexing data: " + str(data) +
                                    " -> For more details see the log messages")

    def index_from_json(self, json_string):
        """
        Indexes the given name and the meta data into elasticsearch.
        Uses or creates the index and type defined in the config

        :param name: Name of the sdearchive dataset (String)
        :param meta_data: Set of meta data (Map)
        :exception: Throws an IndexingException if something went wrong during the request
        """

        data = "No Data"
        try:
            data = json_string
            self.__c_logger.debug("Indexing data: " + str(data))
            self.__f_logger.debug("Indexing data: " + str(data))
            httplib2.debuglevel = 1
            h = httplib2.Http('.cache')
            url = self.__config["host"] + "/" + self.__config["index"] + "/" + self.__config["type"]
            print "DATA->" + data
            print "URL->" + url
            resp, content = h.request(url,
                                      "POST",
                                      data
                                      )
        except Exception as e:
            cache = FailedIndexingCache()
            cache.write_to_cache(data)

            self.__c_logger.exception("ERROR while indexing data: " + str(data) + "\n\n" + e.message)
            self.__f_logger.exception("ERROR while indexing data: " + str(data) + "\n\n" + e.message)
            raise IndexingException("ERROR while indexing data: " + str(data)
                                    + " -> For more details see the log messages")
