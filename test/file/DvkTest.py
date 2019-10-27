import os
import json
import unittest
from file.Dvk import Dvk

class DvkTest(unittest.TestCase):
    """
    Unit tests for the Dvk class.
    
    Attributes:
        dvk (Dvk): Dvk object for testing
    """
    
    def setUp(self):
        """
        Initializes the DvkTest object before unit tests.
        """
        unittest.TestCase.setUp(self)
        self.dvk = Dvk()
    
    def test_constructor(self):
        """
        Tests the Dvk class constructor.
        """
        assert self.dvk.get_title() == ""
        
        #GET FILENAME
        file_path = os.getcwd()
        if "\\" in file_path and not file_path.endswith("\\"):
            file_path = file_path + "\\"
        elif "/" in file_path and not file_path.endswith("/"):
            file_path = file_path + "/"
        file_path = file_path + "writeTest.dvk"
        
        #SET DVK DATA
        self.dvk.set_id("id702")
        self.dvk.set_title("ConstructorTestTitle")
        self.dvk.set_file(file_path)
        self.dvk.write_dvk()
        
        #CHECK VALUES
        loaded_dvk = Dvk(file_path)
        assert loaded_dvk.get_id() == "ID702"
        assert loaded_dvk.get_title() == "ConstructorTestTitle"
        os.remove(file_path)
        
        #CHECK EMPTY
        loaded_dvk = Dvk(None)
        assert loaded_dvk.get_id() == ""
        assert loaded_dvk.get_title() == ""
        assert loaded_dvk.get_artists() == []
        assert loaded_dvk.get_time() == "0000/00/00|00:00"
        assert loaded_dvk.get_web_tags() == []
        assert loaded_dvk.get_description() == ""
        
    def test_read_write_dvk(self):
        """
        Tests the read_dvk and write_dvk methods of the Dvk class.
        """
        #GET FILENAME
        file_path = os.getcwd()
        if "\\" in file_path and not file_path.endswith("\\"):
            file_path = file_path + "\\"
        elif "/" in file_path and not file_path.endswith("/"):
            file_path = file_path + "/"
        file_path = file_path + "writeTest.dvk"
        
        #SET DVK DATA
        self.dvk.set_id("id1234")
        self.dvk.set_title("WriteTestTitle")
        self.dvk.set_artists(["artist", "other artist"])
        self.dvk.set_int_time(1864, 10, 31, 7, 2)
        self.dvk.set_web_tags(["test", "Tags"])
        self.dvk.set_description("<b>desc</b>")
        
        #WRITE THEN READ
        self.dvk.set_file(file_path)
        self.dvk.write_dvk()
        self.dvk.read_dvk()
        os.remove(file_path)
        
        #CHECK VALUES
        assert self.dvk.get_id() == "ID1234"
        assert self.dvk.get_title() == "WriteTestTitle"
        assert self.dvk.get_artists()[0] == "artist"
        assert self.dvk.get_artists()[1] == "other artist"
        assert self.dvk.get_time() == "1864/10/31|07:02"
        assert self.dvk.get_web_tags()[0] == "test"
        assert self.dvk.get_web_tags()[1] == "Tags"
        assert self.dvk.get_description() == "<b>desc</b>"
        
        #CHECK READING NON-EXISTANT FILE
        self.dvk.set_file(None)
        self.dvk.read_dvk()
        assert self.dvk.get_title() == ""
        
        #CHECK READING INVALID FILE
        data = {"test":"nope"}
        try:
            with open(file_path, "w") as out_file:
                json.dump(data, out_file)
                
        except IOError as e:
            print("File error: " + str(e))
    
        self.dvk.read_dvk()
        os.remove(file_path)
        assert self.dvk.get_title() == ""
    
    def test_get_set_file(self):
        """
        Tests the get_file and set_file functions of the Dvk class.
        """
        self.dvk.set_file()
        assert self.dvk.get_file() == ""
        self.dvk.set_file(None)
        assert self.dvk.get_file() == ""
        self.dvk.set_file("test_path.dvk")
        assert self.dvk.get_file() == "test_path.dvk"
        
    def test_get_set_id(self):
        """
        Tests the get_id and set_id functions of the Dvk class.
        """
        self.dvk.set_id()
        assert self.dvk.get_id() == ""
        self.dvk.set_id(None)
        assert self.dvk.get_id() == ""
        self.dvk.set_id("id123")
        assert self.dvk.get_id() == "ID123"
        
    def test_get_set_title(self):
        """
        Tests the get_title and set_title functions of the Dvk class.
        """
        self.dvk.set_title()
        assert self.dvk.get_title() == ""
        self.dvk.set_title(None)
        assert self.dvk.get_title() == ""
        self.dvk.set_title("TestTitle")
        assert self.dvk.get_title() == "TestTitle"
        
    def test_get_set_artists(self):
        """
        Tests the get_artists, set_artists, and set_artist functions of the Dvk class.
        """
        self.dvk.set_artist()
        assert self.dvk.get_artists() == []
        self.dvk.set_artist(None)
        assert self.dvk.get_artists() == []
        self.dvk.set_artist("my_artist")
        assert len(self.dvk.get_artists()) == 1
        assert self.dvk.get_artists()[0] == "my_artist"
        
        self.dvk.set_artists()
        assert self.dvk.get_artists() == []
        self.dvk.set_artists(None)
        assert self.dvk.get_artists() == []
        self.dvk.set_artists(["artist10", "artist10", "", None, "artist1", "test10.0.20-stuff", "test10.0.0-stuff"])
        assert len(self.dvk.get_artists()) == 4
        assert self.dvk.get_artists()[0] == "artist1"
        assert self.dvk.get_artists()[1] == "artist10"
        assert self.dvk.get_artists()[2] == "test10.0.0-stuff"
        assert self.dvk.get_artists()[3] == "test10.0.20-stuff"
    
    def test_set_int_time(self):
        """
        Tests the set_int_time function of the Dvk class.
        """
        self.dvk.set_int_time()
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_int_time(None, None, None, None, None)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        
        #TEST INVALID YEAR
        self.dvk.set_int_time(0, 10, 10, 7, 15)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        
        #TEST INVALID MONTH
        self.dvk.set_int_time(2017, 0, 10, 7, 15)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_int_time(2017, 13, 10, 7, 15)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        
        #TEST INVALID DAY
        self.dvk.set_int_time(2017, 10, 0, 7, 15)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_int_time(2017, 10, 32, 7, 15)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        
        #TEST INVALID HOUR
        self.dvk.set_int_time(2017, 10, 10, -1, 0)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_int_time(2017, 10, 10, 24, 0)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        
        #TEST INVALID MINUTE
        self.dvk.set_int_time(2017, 10, 10, 7, -1)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_int_time(2017, 10, 10, 7, 60)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        
        #TEST VALID TIME
        self.dvk.set_int_time(2017, 10, 10, 7, 0)
        assert self.dvk.get_time() == "2017/10/10|07:00"
        
    def test_get_set_time(self):
        """
        Tests the get_time and set_time functions of the Dvk class.
        """
        self.dvk.set_time()
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_time(None)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_time("2017/10/06")
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_time("yyyy/mm/dd/hh/tt")
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_time("2017!10!06!05!00")
        assert self.dvk.get_time() == "2017/10/06|05:00"
        
    def test_get_set_web_tags(self):
        """
        Tests the get_web_tags and set_web_tags functions of the Dvk class.
        """
        self.dvk.set_web_tags()
        assert self.dvk.get_web_tags() == []
        self.dvk.set_web_tags(None)
        assert self.dvk.get_web_tags() == []
        self.dvk.set_web_tags(["tag1", "Tag2", "other tag", "tag1", None, ""])
        assert len(self.dvk.get_web_tags()) == 3
        assert self.dvk.get_web_tags()[0] == "tag1"
        assert self.dvk.get_web_tags()[1] == "Tag2"
        assert self.dvk.get_web_tags()[2] == "other tag"
        
    def test_get_set_description(self):
        """
        Tests the get_description and set_description functions of the Dvk class.
        """
        self.dvk.set_description()
        assert self.dvk.get_description() == ""
        self.dvk.set_description(None)
        assert self.dvk.get_description() == ""
        self.dvk.set_description("<i>baño</i>")
        assert self.dvk.get_description() == "<i>ba&#241;o</i>"
        
    