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
        assert len(self.dvk.get_title()) == 0
        
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
        assert len(loaded_dvk.get_id()) == 0
        assert len(loaded_dvk.get_title()) == 0
        assert len(loaded_dvk.get_artists()) == 0
        
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
        
        #CHECK READING NON-EXISTANT FILE
        self.dvk.set_file(None)
        self.dvk.read_dvk()
        assert len(self.dvk.get_title()) == 0
        
        #CHECK READING INVALID FILE
        data = {"test":"nope"}
        try:
            with open(file_path, "w") as out_file:
                json.dump(data, out_file)
                
        except IOError as e:
            print("File error: " + str(e))
    
        self.dvk.read_dvk()
        os.remove(file_path)
        assert len(self.dvk.get_title()) == 0
    
    def test_get_set_file(self):
        """
        Tests the get_file and set_file functions of the Dvk class.
        """
        self.dvk.set_file()
        assert len(self.dvk.get_file()) == 0
        self.dvk.set_file(None)
        assert len(self.dvk.get_file()) == 0
        self.dvk.set_file("test_path.dvk")
        assert self.dvk.get_file() == "test_path.dvk"
        
    def test_get_set_id(self):
        """
        Tests the get_id and set_id functions of the Dvk class.
        """
        self.dvk.set_id()
        assert len(self.dvk.get_id()) == 0
        self.dvk.set_id(None)
        assert len(self.dvk.get_id()) == 0
        self.dvk.set_id("id123")
        assert self.dvk.get_id() == "ID123"
        
    def test_get_set_title(self):
        """
        Tests the get_title and set_title functions of the Dvk class.
        """
        self.dvk.set_title()
        assert len(self.dvk.get_title()) == 0
        self.dvk.set_title(None)
        assert len(self.dvk.get_title()) == 0
        self.dvk.set_title("TestTitle")
        assert self.dvk.get_title() == "TestTitle"
        
    def test_get_set_artists(self):
        """
        Tests the get_artists, set_artists, and set_artist functions of the Dvk class.
        """
        self.dvk.set_artist()
        assert len(self.dvk.get_artists()) == 0
        self.dvk.set_artist(None)
        assert len(self.dvk.get_artists()) == 0
        self.dvk.set_artist("my_artist")
        assert len(self.dvk.get_artists()) == 1
        assert self.dvk.get_artists()[0] == "my_artist"
        
        self.dvk.set_artists()
        assert len(self.dvk.get_artists()) == 0
        self.dvk.set_artists(None)
        assert len(self.dvk.get_artists()) == 0
        self.dvk.set_artists(["artist10", "artist10", None, "artist1", "test10.0.0-stuff", "test10.0.20-stuff"])
        assert len(self.dvk.get_artists()) == 4
        assert self.dvk.get_artists()[0] == "artist1"
        assert self.dvk.get_artists()[1] == "artist10"
        assert self.dvk.get_artists()[2] == "test10.0.0-stuff"
        assert self.dvk.get_artists()[3] == "test10.0.20-stuff"
    
    def test_get_set_int_time(self):
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
    