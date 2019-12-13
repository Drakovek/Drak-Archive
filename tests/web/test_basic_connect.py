import unittest
from os import listdir, stat
from pathlib import Path
from shutil import rmtree
from dvk_archive.web.basic_connect import basic_connect
from dvk_archive.web.basic_connect import download
from dvk_archive.web.basic_connect import get_last_modified


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
        try:
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
            url = "http://www.pythonscraping.com/img/gifts/img6.jpg"
            headers = download(url, str(file.absolute()))
            assert file.exists()
            modified = ""
            try:
                modified = headers["Last-Modified"]
            except KeyError:
                pass
            assert modified == "Mon, 04 Aug 2014 00:49:03 GMT"
            assert stat(str(file.absolute())).st_size == 39785
            download(
                url="http://www.pythonscraping.com/img/gifts/img6.jpg",
                filename=str(file.absolute()))
            file = test_dir.joinpath("image(1).jpg")
            assert file.exists()
            assert stat(str(file.absolute())).st_size == 39785
        finally:
            rmtree(test_dir.absolute())

    def test_get_last_modified(self):
        """
        Tests the get_last_modified function.
        """
        assert get_last_modified() == ""
        assert get_last_modified(dict()) == ""
        # TEST INVALID
        dic = {"Last-Modified": ""}
        assert get_last_modified(dic) == ""
        dic = {"Last-Modified": "Mon, BB Aug FFFF GG:TT:PP GMT"}
        assert get_last_modified(dic) == ""
        # TEST ALL MONTHS
        dic = {"Last-Modified": "Udf, 10 Jan 2010 12:05:55 GMT"}
        assert get_last_modified(dic) == "2010/01/10|12:05"
        dic = {"Last-Modified": "Udf, 23 Feb 2015 20:23:55 GMT"}
        assert get_last_modified(dic) == "2015/02/23|20:23"
        dic = {"Last-Modified": "Udf, 01 Mar 2019 12:00:55 GMT"}
        assert get_last_modified(dic) == "2019/03/01|12:00"
        dic = {"Last-Modified": "Udf, 10 Apr 2010 12:05:55 GMT"}
        assert get_last_modified(dic) == "2010/04/10|12:05"
        dic = {"Last-Modified": "Udf, 23 May 2015 20:23:55 GMT"}
        assert get_last_modified(dic) == "2015/05/23|20:23"
        dic = {"Last-Modified": "Udf, 01 Jun 2019 12:00:55 GMT"}
        assert get_last_modified(dic) == "2019/06/01|12:00"
        dic = {"Last-Modified": "Udf, 10 Jul 2010 12:05:55 GMT"}
        assert get_last_modified(dic) == "2010/07/10|12:05"
        dic = {"Last-Modified": "Udf, 23 Aug 2015 20:23:55 GMT"}
        assert get_last_modified(dic) == "2015/08/23|20:23"
        dic = {"Last-Modified": "Udf, 01 Sep 2019 12:00:55 GMT"}
        assert get_last_modified(dic) == "2019/09/01|12:00"
        dic = {"Last-Modified": "Udf, 10 Oct 2010 12:05:55 GMT"}
        assert get_last_modified(dic) == "2010/10/10|12:05"
        dic = {"Last-Modified": "Udf, 23 Nov 2015 20:23:55 GMT"}
        assert get_last_modified(dic) == "2015/11/23|20:23"
        dic = {"Last-Modified": "Udf, 01 Dec 2019 12:00:55 GMT"}
        assert get_last_modified(dic) == "2019/12/01|12:00"
        dic = {"Last-Modified": "Udf, 10 Nop 2010 12:05:55 GMT"}
        assert get_last_modified(dic) == ""
