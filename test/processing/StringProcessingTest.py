import unittest
from processing.StringProcessing import extend_int

class StringProcessingTest(unittest.TestCase):
    """
    Unit tests for the StringProcessing.py module.
    """
    
    def test_extend_int(self):
        """
        Tests the extend_int function in the StringProcessing.py module.
        """
        assert extend_int() == "0"
        assert extend_int(None, 5) == "00000"
        assert extend_int(15, None) == "0"
        assert extend_int(256, 2) == "00"
        assert extend_int(12, 0) == "0"
        assert extend_int(15, 2) == "15"
        assert extend_int(input_int=12, input_length=5) == "00012"