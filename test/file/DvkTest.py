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
        assert loaded_dvk.get_title() == ""
        
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
        
        #WRITE THEN READ
        self.dvk.set_file(file_path)
        self.dvk.write_dvk()
        self.dvk.read_dvk()
        os.remove(file_path)
        
        #CHECK VALUES
        assert self.dvk.get_id() == "ID1234"
        assert self.dvk.get_title() == "WriteTestTitle"
        
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
    