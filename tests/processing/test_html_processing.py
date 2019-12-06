import unittest
from dvk_archive.processing.html_processing import add_escapes
from dvk_archive.processing.html_processing import add_escapes_to_html
from dvk_archive.processing.html_processing import escape_to_char
from dvk_archive.processing.html_processing import replace_escapes


class TestHtmlProcessing(unittest.TestCase):
    """
    Unit tests for the HtmlProcessing.py module.
    """

    def test_add_escapes(self):
        """
        Tests the add_escapes function.
        """
        assert add_escapes() == ""
        assert add_escapes(None) == ""
        output = "&#60;b&#62;Not real html tags&#46;&#60;&#47;b&#62;"
        assert add_escapes("<b>Not real html tags.</b>") == output

    def test_add_escapes_to_html(self):
        """
        Tests the add_escapes_to_html function.
        """
        assert add_escapes_to_html() == ""
        assert add_escapes_to_html(None) == ""
        input = "<a href=\"Sommarfågel\">Sommarfågel</a>"
        output = "<a href=\"Sommarfågel\">Sommarf&#229;gel</a>"
        assert add_escapes_to_html(input) == output
        input = "<a href='Sommarfågel'>Sommarfågel</a>"
        output = "<a href='Sommarfågel'>Sommarf&#229;gel</a>"
        assert add_escapes_to_html(input) == output
        input = "<a href=\"Sommarfågel"
        output = "<a href=\"Sommarfågel"
        assert add_escapes_to_html(input) == output

    def test_escape_to_char(self):
        """
        Tests the escape_to_char function.
        """
        assert escape_to_char() == ""
        assert escape_to_char(None) == ""
        assert escape_to_char("&;") == ""
        assert escape_to_char("apos") == ""
        assert escape_to_char("&nope;") == ""
        assert escape_to_char("&quot;") == "\""
        assert escape_to_char("&apos;") == "'"
        assert escape_to_char("&amp;") == "&"
        assert escape_to_char("&lt;") == "<"
        assert escape_to_char("&gt;") == ">"
        assert escape_to_char("&nbsp;") == " "
        assert escape_to_char("&#60;") == "<"
        assert escape_to_char("&#nope;") == ""

    def test_replace_escapes(self):
        """
        Tests the replace_escapes function.
        """
        assert replace_escapes() == ""
        assert replace_escapes(None) == ""
        input = "&lt;i&gt;Test HTML&#60;&#47;i&#62;"
        assert replace_escapes(input) == "<i>Test HTML</i>"
        input = "this&that"
        assert replace_escapes(input) == "this&that"
        input = "remove&this;"
        assert replace_escapes(input) == "remove"
