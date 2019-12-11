import unittest
from os import listdir, stat
from pathlib import Path
from shutil import rmtree
from dvk_archive.web.basic_connect import basic_connect
from dvk_archive.web.basic_connect import download


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

    def test_download(self):
        """
        Tests the download function.
        """
        test_dir = Path("images")
        test_dir.mkdir(exist_ok=True)
        file = test_dir.joinpath("image.jpg")
        download()
        assert listdir(test_dir.absolute()) == []
        download(url="http://www.pythonscraping.com/img/gifts/img6.jpg")
        assert listdir(test_dir.absolute()) == []
        download(filename=str(file.absolute()))
        assert listdir(test_dir.absolute()) == []
        download(
            url="asfdwersdbsdfsd",
            filename=str(file.absolute()))
        assert listdir(test_dir.absolute()) == []
        download(
            url="http://www.pythonscraping.com/img/gifts/img6.jpg",
            filename=str(file.absolute()))
        assert file.exists()
        assert stat(str(file.absolute())).st_size == 39785
        download(
            url="http://www.pythonscraping.com/img/gifts/img6.jpg",
            filename=str(file.absolute()))
        file = test_dir.joinpath("image(1).jpg")
        assert file.exists()
        assert stat(str(file.absolute())).st_size == 39785
        download()
        rmtree(test_dir.absolute())
