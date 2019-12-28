import unittest
from os import listdir, stat
from pathlib import Path
from shutil import rmtree
from dvk_archive.web.basic_connect import bs_connect
from dvk_archive.web.basic_connect import json_connect
from dvk_archive.web.basic_connect import basic_connect
from dvk_archive.web.basic_connect import download
from dvk_archive.web.basic_connect import get_last_modified
from dvk_archive.web.basic_connect import remove_header_footer


class TestBasicConnect(unittest.TestCase):
    """
    Unit tests for the basic_connect.py module.
    """

    def test_bs_connect(self):
        """
        Tests the bs_connect function.
        """
        assert bs_connect() is None
        assert bs_connect(None) is None
        assert bs_connect("") is None
        assert bs_connect("jkslkeerkn") is None
        assert bs_connect("http://lakjwj;wklk;okjovz") is None
        url = "http://pythonscraping.com/exercises/exercise1.html"
        bs = bs_connect(url)
        assert bs is not None
        assert bs.find("h1").get_text() == "An Interesting Title"
        url = "https://mangadex.org/title/27152/jojo"
        bs = bs_connect(url)
        d = ""
        assert bs is not None
        bs_list = bs.findAll("div", {"class": "col-lg-3 col-xl-2 strong"})
        for item in bs_list:
            if item.get_text() == "Description:":
                sibling = item.find_next_sibling("div")
                d = remove_header_footer(str(sibling))
                break
        desc = "Second story arc of JoJo no Kimyou na Bouken series."
        desc = desc + "<br/><br/>Takes place in the 1930s"
        assert d.startswith(desc)

    def test_json_connect(self):
        # TEST JSON
        json = json_connect("http://echo.jsontest.com/key/test/next/blah")
        assert json is not None
        assert json["key"] == "test"
        assert json["next"] == "blah"
        # TEST NON-JSON
        url = "http://pythonscraping.com/exercises/exercise1.html"
        json = json_connect(url)
        print(type(json))
        assert json is None
        # TEST INVALID
        assert json_connect() is None

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
        html = basic_connect(url)
        assert html is not None
        assert html.startswith("<html>\n<head>\n<title>A Useful Page</title>")

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

    def test_remove_header_footer(self):
        """
        Tests the remove_header_footer function.
        """
        assert remove_header_footer() == ""
        assert remove_header_footer("") == ""
        assert remove_header_footer("   ") == ""
        assert remove_header_footer("<p>") == ""
        assert remove_header_footer("<head><foot>") == ""
        assert remove_header_footer("<p>  test") == "test"
        assert remove_header_footer("test </p>") == "test"
        assert remove_header_footer("<head> Things   </foot>") == "Things"
        assert remove_header_footer("<div><p>bleh</p></div>") == "<p>bleh</p>"
