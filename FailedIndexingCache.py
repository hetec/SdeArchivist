# -*- encoding utf-8 -*-
import os

class FailedIndexingCache:
    """
    File cache to hold failed indexing trials. These stored information can be
    reused to index the failed data on a new run of the script
    """
    def __init__(self, cache_file="config/failed_indexing.cache"):
        """
        Creates a predefined cache

        :param cache_file: Path to the cache file (String)
        """
        self.__CACHE_FILE = cache_file

    def write_to_cache(self, content):
        """
        Writes on line to the cache

        :param content: The content (String)
        """
        self.__write('a', content)

    def write_all_to_cache(self, contents):
        """
        Writes several lines to the cache
        :param contents: List of lines (List)
        """
        for line in contents:
            self.__write('a', line)

    def read_from_cache(self):
        """
        Reads all lines of the cache into a list

        :return: (List)
        """
        if os.path.isfile(self.__CACHE_FILE):
            file_con = None
            try:
                file_con = open(self.__CACHE_FILE, 'r')
                entries = file_con.readlines()
                return entries
            except Exception as e:
                raise EnvironmentError("Cannot write to cache: " + str(e))
            finally:
                file_con.close()

    def clear_cache(self):
        """
        Empties the cache file
        """
        self.__write('w', delimiter="")

    def __write(self, mode, content="", delimiter="\n"):
        file_con = None
        try:
            file_con = open(self.__CACHE_FILE, mode)
            file_con.write(content + delimiter)
        except Exception as e:
            raise EnvironmentError("Cannot write to cache: " + str(e))
        finally:
            file_con.close()