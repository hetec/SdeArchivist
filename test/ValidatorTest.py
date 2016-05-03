import unittest
from MetaDataValidator import MetaDataValidator
from MetaDataTag import MetaDataTag
from MetaData import MetaData
from mock import MagicMock
import logging

class ValidationTest(unittest.TestCase):

    # Mocks
    c_logger = logging.getLogger("mock")
    f_logger = logging.getLogger("mock")

    tag_not_empty_mapped = MetaDataTag("test1", False, "mapped1")
    tag_not_empty_not_mapped = MetaDataTag("test2", False)
    tag_empty_not_mapped = MetaDataTag("test3", True)
    tag_empty_mapped = MetaDataTag("test4", True, "mapped4")
    tag_empty_attribute = MetaDataTag("test5", True, mapped_name="", attributes=["attr51", "attr52"])
    tag_not_empty_attribute = MetaDataTag("test6", False, mapped_name="", attributes=["attr6"])
    unique_nest_tag_not_empty = MetaDataTag("unique_inner", False, mapped_name="")
    multi_nest_tag_not_empty_1 = MetaDataTag("multi_inner", False, mapped_name="")
    multi_nest_tag_not_empty_2 = MetaDataTag("multi_inner", False, mapped_name="")
    multi_nest_tag_not_empty_path1 = MetaDataTag("test7/multi_inner", False, mapped_name="")
    multi_nest_tag_not_empty_path2 = MetaDataTag("test8/multi_inner", False, mapped_name="")

    x = '''
    <root>
        <test1>Not empty</test1>
        <test2>Not empty</test2>
        <test3/>
        <test4/>
        <test5 attr51="attr5" attr52="attr52" />
        <test6 attr6="attr6">Not empty</test6>
        <test7>
            <unique_inner>Not empty</unique_inner>
            <multi_inner></multi_inner>
        </test7>
        <test8>
            <multi_inner>Not empty</multi_inner>
        </test8>
    </root>
    '''

    # Positive tests

    def test_validate_defaultXmlTags_validMetaData(self):
        tags = {"test1": self.tag_not_empty_mapped,
                "test3": self.tag_empty_not_mapped}
        validator = MetaDataValidator(self.x, tags)
        validator.set_console_logger(self.c_logger)
        validator.set_file_logger(self.f_logger)

        meta = MetaData()
        validator.validate(meta)
        self.assertEqual(meta.is_valid(), True, "Invalid tags")

    def test_validate_defaultXmlTags_correctMappedNames(self):
        tags = {"test1": self.tag_not_empty_mapped,
                "test4": self.tag_empty_mapped}
        validator = MetaDataValidator(self.x, tags)
        validator.set_console_logger(self.c_logger)
        validator.set_file_logger(self.f_logger)

        meta = MetaData()
        validator.validate(meta)
        if "mapped1" not in meta.meta_data_info() or "mapped4" not in meta.meta_data_info():
            raise Exception("Meta data name was not mapped correctly")

    def test_validate_defaultEmptyXmlTagsWithAttributes_validMetaData(self):
        tags = {"test5": self.tag_empty_attribute,
                "test6": self.tag_not_empty_attribute}
        validator = MetaDataValidator(self.x, tags)
        validator.set_console_logger(self.c_logger)
        validator.set_file_logger(self.f_logger)

        meta = MetaData()
        validator.validate(meta)
        self.assertEqual(meta.is_valid(), True, "Invalid tags")

    def test_validate_uniqueNestedTagsWithoutPathDefinition_validMetaData(self):
        tags = {"unique_inner": self.unique_nest_tag_not_empty}
        validator = MetaDataValidator(self.x, tags)
        validator.set_console_logger(self.c_logger)
        validator.set_file_logger(self.f_logger)

        meta = MetaData()
        validator.validate(meta)
        self.assertEqual(meta.is_valid(), True, "Invalid tags")

    def test_validate_mulitNestedTagsWithoutPathDefinition_noDistinctionFailsAlwaysIfOneFails(self):
        tags = {"multi_inner": self.multi_nest_tag_not_empty_1}
        validator = MetaDataValidator(self.x, tags)
        validator.set_console_logger(self.c_logger)
        validator.set_file_logger(self.f_logger)

        meta = MetaData()
        validator.validate(meta)
        self.assertNotEqual(meta.is_valid(), True, "Tags must not be valid because one is invalid")

    def test_validate_mulitNestedTagsWithPathDefinition_validMetaTag(self):
        tags = {"test8/multi_inner": self.multi_nest_tag_not_empty_path2}
        validator = MetaDataValidator(self.x, tags)
        validator.set_console_logger(self.c_logger)
        validator.set_file_logger(self.f_logger)

        meta = MetaData()
        validator.validate(meta)
        self.assertEqual(meta.is_valid(), True, "Invalid tags")

    def test_validate_mappedTagsWithAttributes_metaDataHasTheRightContent(self):
        tags = {"test1": self.tag_not_empty_mapped,
                "test5": self.tag_empty_attribute}
        validator = MetaDataValidator(self.x, tags)
        validator.set_console_logger(self.c_logger)
        validator.set_file_logger(self.f_logger)

        meta = MetaData()
        validator.validate(meta)
        self.assertEqual(meta.is_valid(), True, "Invalid tags")
        #should_exist = [""]


if __name__ == "__main__":
    unittest.main()