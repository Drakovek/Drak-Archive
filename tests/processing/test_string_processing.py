import unittest
from dvk_archive.processing.string_processing import extend_int
from dvk_archive.processing.string_processing import get_extension


class TestStringProcessing(unittest.TestCase):
    """
    Unit tests for the StringProcessing.py module.
    """

    def test_extend_int(self):
        """
        Tests the extend_int function.
        """
        assert extend_int() == "0"
        assert extend_int(None, 5) == "00000"
        assert extend_int(15, None) == "0"
        assert extend_int(256, 2) == "00"
        assert extend_int(12, 0) == "0"
        assert extend_int(15, 2) == "15"
        assert extend_int(input_int=12, input_length=5) == "00012"

    def test_get_extension(self):
        assert get_extension() == ""
        assert get_extension(None) == ""
        assert get_extension("") == ""
        assert get_extension("test") == ""
        assert get_extension("http://url.com/linksNstuff") == ""
        assert get_extension("/dot.folder/file.py") == ".py"
        assert get_extension("file.txt") == ".txt"
        assert get_extension("http://url.com/linksNstuff/file.png") == ".png"
