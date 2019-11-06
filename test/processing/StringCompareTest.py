import unittest
from processing.StringCompare import compare_strings, get_section, is_digit, compare_sections, is_number_string, compare_alphanum

class StringCompareTest(unittest.TestCase):
    """
    Unit tests for the StringCompare.py module.
    """
    
    def test_compare_strings(self):
        """
        Tests the compare_strings function of the StringCompare.py module.
        """
        assert compare_strings() == 0
        assert compare_strings(None, "a") == 0
        assert compare_strings("b", None) == 0
        assert compare_strings(None, None) == 0
        assert compare_strings("B", "a") == 1
        assert compare_strings("a", "B") == -1
        assert compare_strings("Test1", "Test2") == -1
        assert compare_strings("Same", "same") == 0
        
    def test_compare_alphanum(self):
        """
        Tests the compare_alphanum function of the StringCompare.py module.
        """
        assert compare_alphanum() == 0
        assert compare_alphanum(None, "a") == 0
        assert compare_alphanum("b", None) == 0
        assert compare_alphanum(None, None) == 0
        assert compare_alphanum("B", "a") == 1
        assert compare_alphanum("a", "B") == -1
        assert compare_alphanum("Test1", "Test2") == -1
        assert compare_alphanum("string 100", "String 2") == 1
        assert compare_alphanum("Same25", "same25") == 0
        assert compare_alphanum("Test 0.5", "Test 0,05") == 1
        assert compare_alphanum("v1.2.10", "v1.2.02") == 1
        assert compare_alphanum("Thing 5 Extra", "Thing 20") == -1
    
    def test_get_section(self):
        """
        Tests the get_section function of the StringCompare.py module.
        """
        assert get_section() == ""
        assert get_section("") == ""
        assert get_section(None) == ""
        assert get_section("Some Text") == "Some Text"
        assert get_section("Test#1 - Other") == "Test#"
        assert get_section("256") == "256"
        assert get_section("15 Thing") == "15"
        assert get_section("10.5") == "10"
        assert get_section(".25 Text") == ".25"
        assert get_section(",50.2 Thing") == ",50"
        assert get_section("Test, and stuff.!") == "Test, and stuff.!"
        assert get_section("Number: .02!") == "Number: "
        assert get_section("# ,40") == "# "
    
    def test_is_digit(self):
        """
        Tests the is_digit function of the StringCompare.py module.
        """
        assert is_digit() == False
        assert is_digit("") == False
        assert is_digit(None) == False
        assert is_digit("long") == False
        assert is_digit("0") == True
        assert is_digit("9") == True
        assert is_digit("5") == True
        assert is_digit("/") == False
        assert is_digit(":") == False
        assert is_digit("A") == False
        
    def test_is_number_string(self):
        """
        Tests the is_number_string function of the StringCompare.py module.
        """
        assert is_number_string() == False
        assert is_number_string("") == False
        assert is_number_string(None) == False
        assert is_number_string("string02") == False
        assert is_number_string("25 Thing") == True
        assert is_number_string(".34 String") == True
        assert is_number_string(",53.4") == True
        assert is_number_string(".not number") == False
        assert is_number_string(", nope") == False
        
    def test_compare_sections(self):
        """
        Tests the compare_sections function of the StringCompare.py module.
        """
        assert compare_sections() == 0
        assert compare_sections("", "a") == -1
        assert compare_sections("word", "") == 1
        assert compare_sections("text", "58") == 1
        assert compare_sections("24", "string") == -1
        assert compare_sections("2.5", "2.5") == 0
        assert compare_sections("10", "1") == 1
        assert compare_sections("10.05", "010.5") == -1
        assert compare_sections(".2", ".02") == 1
        assert compare_sections("10,05", "010,5") == -1
        assert compare_sections(",2", ",02") == 1
        assert compare_sections("0000000001", "0") == 1
        assert compare_sections("12.05.03", "2") == 0
        assert compare_sections("12345678900000000000000000000000000000000000000000000", 
                                "12345678900000000000000000000000000000000000000000001") == -1
        assert compare_sections("0.12345678900000000000000000000000000000000000000000000", 
                                "0.12345678900000000000000000000000000000000000000000001") == -1
        
        