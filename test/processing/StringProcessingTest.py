import unittest
from processing.StringProcessing import extend_int

class StringProcessingTest(unittest.TestCase):
    def test_extend_int(self):
        assert extend_int() == "0"
        assert extend_int(None, 5) == "00000"
        assert extend_int(15, None) == "0"
        assert extend_int(256, 2) == "00"
        assert extend_int(12, 0) == "0"
        assert extend_int(15, 2) == "15"
        assert extend_int(input_int=12, input_length=5) == "00012"