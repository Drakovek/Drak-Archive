import unittest
from processing.ListProcessing import clean_list

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