# -*- encoding utf-8 -*-
import os

class IndexRepeater:

    def __init__(self, cache, indexer):
        self.__cache = cache
        self.__indexer = indexer

    def reindex(self):
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
        return line[:-1]
