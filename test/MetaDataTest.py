import unittest
from MetaData import MetaData

class MetaDataTest(unittest.TestCase):

    def test_replaceExistingName_twoDuplicatesInMap_AppendNumberThreeToTheName(self):
        meta_data = MetaData()
        meta_data.add_meta_data("Original", "Original")
        meta_data.add_meta_data("Original", "Original1")
        meta_data.add_meta_data("Original", "Original2")
        meta_data.add_meta_data("Original", "Original3")
        self.assertEqual(len((meta_data.meta_data())['Original']), 4, "Wrong number of elements in list")

    def test_replaceExistingName_noDuplicate_originalNameUsed(self):
        meta_data = MetaData()
        meta_data.add_meta_data("Original", "Original")
        meta_data.add_meta_data("Original", "Original1")
        meta_data.add_meta_data("Original_X", "OriginalX")

        self.assertEqual(len((meta_data.meta_data())['Original']), 2, "Wrong number of elements in list")
        self.assertEqual((meta_data.meta_data())['Original_X'], "OriginalX", "Wrong name")


if __name__ == "__main__":
    unittest.main()