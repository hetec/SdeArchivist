import unittest
from IndexRepeater import IndexRepeater
import mock
from FailedIndexingCache import FailedIndexingCache
from DataIndexer import DataIndexer


class IndexRepeaterTest(unittest.TestCase):

    @mock.patch("IndexRepeaterTest.FailedIndexingCache")
    @mock.patch("IndexRepeaterTest.DataIndexer")
    def setUp(self, mock_indexer, mock_cache):
        self.cache = FailedIndexingCache()
        self.indexer = DataIndexer(None)

        self.instance = mock_cache.return_value
        self.indexer_instance = mock_indexer.return_value

    def test_repeat_indexing_on_data_available_throw_no_exception(self):
        self.instance.read_from_cache.return_value = ["lineOne\n", "lineTwo\n"]

        repeater = IndexRepeater(self.cache, self.indexer)
        repeater.reindex()

        self.cache.read_from_cache.assert_called_once()
        self.cache.clear_cache.assert_any_call()
        self.indexer.index_from_json.assert_any_call("lineTwo")
        self.indexer.index_from_json.assert_any_call("lineOne")

    def test_repeat_indexing_empty_lines_are_skipped(self):
        self.instance.read_from_cache.return_value = ["   "]

        repeater = IndexRepeater(self.cache, self.indexer)
        repeater.reindex()

        self.cache.clear_cache.assert_called_once()
        self.assertFalse(self.indexer.index_from_json.called)


if __name__ == "__main__":
    unittest.main()