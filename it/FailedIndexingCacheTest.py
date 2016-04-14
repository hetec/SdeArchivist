import unittest
import os
from FailedIndexingCache import FailedIndexingCache

class FailedIndexingCacheTest(unittest.TestCase):

    def setUp(self):
        try:
            os.remove("./test.cache")
        except:
            print "no file"
        self.cache = FailedIndexingCache("test.cache")

    def tearDown(self):
        self.cache = None
        try:
            os.remove("./test.cache")
        except:
            print "no file"

    def test_reading_particular_written_lines_from_cache_multiple_lines_returns_list_of_these_lines(self):
        self.cache.write_to_cache("Test line one")
        self.cache.write_to_cache("Test line two")

        entries = self.cache.read_from_cache()
        self.assertEqual(len(entries), 2)

    def test_reading_multiple_written_lines_from_cache_multiple_lines_returns_list_of_these_lines(self):
        self.cache.write_all_to_cache(["Test line one", "Test line two"])

        entries = self.cache.read_from_cache()
        self.assertEqual(len(entries), 2)

    def test_clear_cache_on_data_available_empties_the_file(self):
        self.cache.write_all_to_cache(["Test line one", "Test line two"])

        entries_before = self.cache.read_from_cache()
        self.cache.clear_cache()
        entries_after = self.cache.read_from_cache()

        self.assertEqual(len(entries_before), 2)
        self.assertEqual(len(entries_after), 0)

if __name__ == "__main__":
    unittest.main()