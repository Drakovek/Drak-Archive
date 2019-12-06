import unittest
from dvk_archive.web.basic_connect import basic_connect


class TestBasicConnect(unittest.TestCase):
    """
    Unit tests for the basic_connect.py module.
    """

    def test_basic_connect(self):
        """
        Tests the basic_connect function.
        """
        assert basic_connect() is None
        assert basic_connect(None) is None
        assert basic_connect("") is None
        assert basic_connect("jkslkeerkn") is None
        assert basic_connect("http://lakjwj;wklk;okjovz") is None
        url = "http://pythonscraping.com/exercises/exercise1.html"
        bs = basic_connect(url)
        if bs is None:
            assert False
        else:
            assert bs.find("h1").get_text() == "An Interesting Title"
