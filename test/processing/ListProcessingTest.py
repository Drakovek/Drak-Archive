import unittest
from processing.ListProcessing import clean_list, list_to_string

class ListProcessingTest(unittest.TestCase):
    """
    Unit tests for the ListProcessing.py module.
    """
    
    def test_clean_list(self):
        """
        Tests the clean_list function in the ListProcessing.py module.
        """
        assert len(clean_list()) == 0
        assert len(clean_list(None)) == 0
        cleaned = clean_list(["these", "are", "things", "", None, "are"])
        assert len(cleaned) == 3
        assert cleaned[0] == "these"
        assert cleaned[1] == "are"
        assert cleaned[2] == "things"
        
    def test_list_to_string(self):
        """
        Tests the list_to_string function in the ListProcessing.py module.
        """
        assert list_to_string() == ""
        assert list_to_string(None) == ""
        assert list_to_string([""]) == ""
        assert list_to_string([None]) == ""
        assert list_to_string(["test"]) == "test"
        assert list_to_string(["", "String1", None, None, "string 2", "3"]) == "String1,string 2,3"
        
        