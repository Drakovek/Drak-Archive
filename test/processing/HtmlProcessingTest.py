import unittest
from processing.HtmlProcessing import add_escapes, escape_to_char, replace_escapes, add_escapes_to_html

class HtmlProcessingTest(unittest.TestCase):
    """
    Unit tests for the HtmlProcessing.py module.
    """
    
    def test_add_escapes(self):
        """
        Tests the add_escapes function of the HtmlProcessing.py module.
        """
        assert add_escapes() == ""
        assert add_escapes(None) == ""
        assert add_escapes("<b>Not real html tags.</b>") == "&#60;b&#62;Not real html tags&#46;&#60;&#47;b&#62;"

    def test_add_escapes_to_html(self):
        """
        Tests the add_escapes_to_html function of the HtmlProcessing.py module.
        """
        assert add_escapes_to_html() == ""
        assert add_escapes_to_html(None) == ""
        assert add_escapes_to_html("<a href=\"Sommarfågel\">Sommarfågel</a>") == "<a href=\"Sommarfågel\">Sommarf&#229;gel</a>"
        assert add_escapes_to_html("<a href='Sommarfågel'>Sommarfågel</a>") == "<a href='Sommarfågel'>Sommarf&#229;gel</a>"
        assert add_escapes_to_html("<a href=\"Sommarfågel") == "<a href=\"Sommarfågel"
    
    def test_escape_to_char(self):
        """
        Tests the escape_to_char function of the HtmlProcessing.py module.
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
        
    def test_replace_escapes(self):
        """
        Tests the replace_escapes function of the HtmlProcessing.py module.
        """
        assert replace_escapes() == ""
        assert replace_escapes(None) == ""
        assert replace_escapes("&lt;i&gt;Test HTML&#60;&#47;i&#62;") == "<i>Test HTML</i>"
        assert replace_escapes("this&that") == "this&that"
        assert replace_escapes("remove&this;") == "remove"
    