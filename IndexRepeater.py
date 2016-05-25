# -*- encoding utf-8 -*-
import os

class IndexRepeater:
    """
    Enables the indexation of failed indexing attempts
    """

    def __init__(self, cache, indexer):
        self.__cache = cache
        self.__indexer = indexer

    def reindex(self):
        """
        Indexes all entries of FailedIndexingCache
        """
        entries = self.__cache.read_from_cache()
        self.__cache.clear_cache()
        if entries:
            for entry in entries:
                if len(entry.strip()) > 0:
                    try:
                        self.__indexer.index_from_json(self.trim_line_break(str(entry)))
                    except Exception as e:
                        print(e)

    def trim_line_break(self, line):
        """
        removes the line break

        :param line: One line of the cache file
        :return: Line without line break
        """

        return line[:-1]
