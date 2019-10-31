import os
import json
import unittest
from file.Dvk import Dvk
from pathlib import Path

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
        #CHECK EMPTY
        assert self.dvk.get_title() == ""
        assert self.dvk.get_id() == ""
        assert self.dvk.get_title() == ""
        assert self.dvk.get_artists() == []
        assert self.dvk.get_time() == "0000/00/00|00:00"
        assert self.dvk.get_web_tags() == []
        assert self.dvk.get_description() == ""
        assert self.dvk.get_page_url() == ""
        assert self.dvk.get_direct_url() == ""
        assert self.dvk.get_secondary_url() == ""
        assert self.dvk.get_media_file() == None
        assert self.dvk.get_secondary_file() == None
        assert self.dvk.get_previous_ids() == None
        assert self.dvk.get_next_ids() == None
        assert self.dvk.get_section_first() == False
        assert self.dvk.get_section_last() == False
        assert self.dvk.get_sequence_title() == ""
        assert self.dvk.get_section_title() == ""
        
        #GET FILENAME
        file_path = Path("writeTest.dvk").absolute()
        
        #SET DVK DATA
        self.dvk.set_id("id702")
        self.dvk.set_title("ConstructorTestTitle")
        self.dvk.set_artist("artistName")
        self.dvk.set_page_url("/url/")
        self.dvk.set_file(file_path)
        self.dvk.set_media_file("media.jpg")
        self.dvk.write_dvk()
        
        #CHECK VALUES
        loaded_dvk = Dvk(file_path)
        assert loaded_dvk.get_id() == "ID702"
        assert loaded_dvk.get_title() == "ConstructorTestTitle"
        assert loaded_dvk.get_artists()[0] == "artistName"
        assert loaded_dvk.get_page_url() == "/url/"
        assert loaded_dvk.get_media_file().name == "media.jpg"
        os.remove(file_path)
        
    def test_read_write_dvk(self):
        """
        Tests the read_dvk and write_dvk methods of the Dvk class.
        """
        #GET FILENAME
        file_path = Path("writeTest.dvk").absolute()
        
        #SET DVK DATA
        self.dvk.set_file(file_path)
        self.dvk.set_id("id1234")
        self.dvk.set_title("WriteTestTitle")
        self.dvk.set_artists(["artist", "other artist"])
        self.dvk.set_int_time(1864, 10, 31, 7, 2)
        self.dvk.set_web_tags(["test", "Tags"])
        self.dvk.set_description("<b>desc</b>")
        self.dvk.set_page_url("http://somepage.com")
        self.dvk.set_direct_url("http://image.png")
        self.dvk.set_secondary_url("https://other.png")
        self.dvk.set_media_file("media.png")
        self.dvk.set_secondary_file("2nd.jpeg")
        self.dvk.set_previous_ids(["Last1", "last2"])
        self.dvk.set_next_ids(["next1", "Next2"])
        self.dvk.set_section_first(True)
        self.dvk.set_section_last(True)
        self.dvk.set_sequence_title("Seq Title")
        self.dvk.set_section_title("Section")
        
        #WRITE THEN READ
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
        assert self.dvk.get_page_url() == "http://somepage.com"
        assert self.dvk.get_direct_url() == "http://image.png"
        assert self.dvk.get_secondary_url() == "https://other.png"
        assert self.dvk.get_media_file().name == "media.png"
        assert self.dvk.get_secondary_file().name == "2nd.jpeg"
        assert self.dvk.get_previous_ids()[0] == "LAST1"
        assert self.dvk.get_previous_ids()[1] == "LAST2"
        assert self.dvk.get_next_ids()[0] == "NEXT1"
        assert self.dvk.get_next_ids()[1] == "NEXT2"
        assert self.dvk.get_section_first() == True
        assert self.dvk.get_section_last() == True
        assert self.dvk.get_sequence_title() == "Seq Title"
        assert self.dvk.get_section_title() == "Section"
        
        #CHECK SEQUENCE WRITING
        self.dvk.set_previous_ids(None)
        self.dvk.set_next_ids(None)
        self.dvk.write_dvk()
        self.dvk.read_dvk()
        assert self.dvk.get_previous_ids() == None
        assert self.dvk.get_next_ids() == None
        self.dvk.set_previous_ids([])
        self.dvk.set_next_ids([])
        self.dvk.write_dvk()
        self.dvk.read_dvk()
        assert self.dvk.get_previous_ids() == []
        assert self.dvk.get_next_ids() == []
        
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
        
        #CHECK WRITING INVALID FILE
        invalid_dvk = Dvk()
        invalid_path = Path("nonExistant.dvk")
        invalid_dvk.set_file(invalid_path.absolute())
        assert not invalid_path.exists()
    
    def test_can_write(self):
        """
        Tests the can_write function of the Dvk class.
        """
        self.dvk.set_file("not_real.dvk")
        self.dvk.set_id("id")
        self.dvk.set_title("title")
        self.dvk.set_artist("artist")
        self.dvk.set_page_url("page_url")
        self.dvk.set_media_file("media.png")
        assert self.dvk.can_write()
        self.dvk.set_file()
        assert not self.dvk.can_write()
        self.dvk.set_file("file.dvk")
        self.dvk.set_id()
        assert not self.dvk.can_write()
        self.dvk.set_id("id")
        self.dvk.set_title()
        assert not self.dvk.can_write()
        self.dvk.set_title("title")
        self.dvk.set_artist()
        assert not self.dvk.can_write()
        self.dvk.set_artist("artist")
        self.dvk.set_page_url()
        assert not self.dvk.can_write()
        self.dvk.set_page_url("page_url")
        self.dvk.set_media_file()
        assert not self.dvk.can_write()
        
    def test_get_set_file(self):
        """
        Tests the get_file and set_file functions of the Dvk class.
        """
        self.dvk.set_file()
        assert self.dvk.get_file() == None
        self.dvk.set_file(None)
        assert self.dvk.get_file() == None
        self.dvk.set_file("")
        assert self.dvk.get_file() == None
        self.dvk.set_file("test_path.dvk")
        assert self.dvk.get_file().name == "test_path.dvk"
        
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
        self.dvk.set_description("<i>Baño</i>")
        assert self.dvk.get_description() == "<i>Ba&#241;o</i>"
        
    def test_get_set_page_url(self):
        """
        Tests the get_page_url and set_page_url functions of the Dvk class.
        """
        self.dvk.set_page_url()
        assert self.dvk.get_page_url() == ""
        self.dvk.set_page_url(None)
        assert self.dvk.get_page_url() == ""
        self.dvk.set_page_url("/Page/url")
        assert self.dvk.get_page_url() == "/Page/url"
    
    def test_get_set_direct_url(self):
        """
        Tests the get_direct_url and set_direct_url functions of the Dvk class.
        """
        self.dvk.set_direct_url()
        assert self.dvk.get_direct_url() == ""
        self.dvk.set_direct_url(None)
        assert self.dvk.get_direct_url() == ""
        self.dvk.set_direct_url("/direct/URL")
        assert self.dvk.get_direct_url() == "/direct/URL"
        
    def test_get_set_secondary_url(self):
        """
        Tests the get_secondary_url and set_secondary_url functions of the Dvk class.
        """
        self.dvk.set_secondary_url()
        assert self.dvk.get_secondary_url() == ""
        self.dvk.set_secondary_url(None)
        assert self.dvk.get_secondary_url() == ""
        self.dvk.set_secondary_url("/Secondary/Url")
        assert self.dvk.get_secondary_url() == "/Secondary/Url"
        
    def test_get_set_media_file(self):
        """
        Tests the get_media_file and set_media_file functions of the Dvk class.
        """
        self.dvk.set_media_file("bleh.png")
        assert self.dvk.get_media_file() == None
        self.dvk.set_file(Path("media.dvk").absolute())
        self.dvk.set_media_file("media.png")
        assert self.dvk.get_media_file().name == "media.png"
        assert self.dvk.get_file().parent == self.dvk.get_media_file().parent
        self.dvk.set_media_file()
        assert self.dvk.get_media_file() == None
        self.dvk.set_media_file(None)
        assert self.dvk.get_media_file() == None
        self.dvk.set_media_file("")
        assert self.dvk.get_media_file() == None
        
    def test_get_set_secondary_file(self):
        """
        Tests the get_secondary_file and set_secondary_file functions of the Dvk class.
        """
        self.dvk.set_secondary_file("other.png")
        assert self.dvk.get_media_file() == None
        self.dvk.set_file(Path("mine.dvk").absolute())
        self.dvk.set_secondary_file("second.png")
        assert self.dvk.get_secondary_file().name == "second.png"
        assert self.dvk.get_file().parent == self.dvk.get_secondary_file().parent
        self.dvk.set_secondary_file()
        assert self.dvk.get_secondary_file() == None
        self.dvk.set_secondary_file("")
        assert self.dvk.get_secondary_file() == None
        self.dvk.set_secondary_file(None)
        assert self.dvk.get_secondary_file() == None

    def test_get_set_previous_ids(self):
        """
        Tests the get_previous_ids and set_previous_ids functions of the Dvk class.
        """
        self.dvk.set_previous_ids()
        assert self.dvk.get_previous_ids() == None
        self.dvk.set_previous_ids(None)
        assert self.dvk.get_previous_ids() == None
        self.dvk.set_previous_ids([])
        assert self.dvk.get_previous_ids() == []
        self.dvk.set_previous_ids(["id1", "", "id2"])
        assert self.dvk.get_previous_ids() == []
        self.dvk.set_previous_ids(["id1", "id2", None])
        assert self.dvk.get_previous_ids() == []
        self.dvk.set_previous_ids(["id1", "Id2"])
        assert len(self.dvk.get_previous_ids()) == 2
        assert self.dvk.get_previous_ids()[0] == "ID1"
        assert self.dvk.get_previous_ids()[1] == "ID2"
    
    def test_get_set_next_ids(self):
        """
        Tests the get_next_ids and set_next_ids functions of the Dvk class.
        """
        self.dvk.set_next_ids()
        assert self.dvk.get_next_ids() == None
        self.dvk.set_next_ids(None)
        assert self.dvk.get_next_ids() == None
        self.dvk.set_next_ids([])
        assert self.dvk.get_next_ids() == []
        self.dvk.set_next_ids(["", "one", "two"])
        assert self.dvk.get_next_ids() == []
        self.dvk.set_next_ids(["one", "two", None])
        assert self.dvk.get_next_ids() == []
        self.dvk.set_next_ids(["One", "two"])
        assert len(self.dvk.get_next_ids()) == 2
        assert self.dvk.get_next_ids()[0] == "ONE"
        assert self.dvk.get_next_ids()[1] == "TWO"
        
    def test_get_set_section_first(self):
        """
        Tests the get_section_first and set_section_first functions of the Dvk class.
        """
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first() == False
        #MISSING SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first() == False
        self.dvk.set_previous_ids()
        self.dvk.set_next_ids(["ID2"])
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first() == False
        #FULL SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first() == True
        #LAST/FIRST IN SEQUENCE
        self.dvk.set_previous_ids([])
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first() == True
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_next_ids([])
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first() == True
        #SINGLE
        self.dvk.set_previous_ids([])
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first() == False
        #INVALID AFTER SETTING
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first() == True
        self.dvk.set_previous_ids([])
        assert self.dvk.get_section_first() == False
        self.dvk.set_previous_ids("ID1")
        self.dvk.set_next_ids("ID2")
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first() == True
        self.dvk.set_previous_ids()
        assert self.dvk.get_section_first() == False
           
    def test_get_set_section_last(self):
        """
        Tests the get_section_last and set_section_last functions of the Dvk class.
        """
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last() == False
        #MISSING SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last() == False
        self.dvk.set_previous_ids()
        self.dvk.set_next_ids(["ID2"])
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last() == False
        #FULL SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last() == True
        #LAST/FIRST IN SEQUENCE
        self.dvk.set_previous_ids([])
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last() == True
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_next_ids([])
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last() == True
        #SINGLE
        self.dvk.set_previous_ids([])
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last() == False
        #INVALID AFTER SETTING
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last() == True
        self.dvk.set_previous_ids([])
        assert self.dvk.get_section_last() == False
        self.dvk.set_previous_ids("ID1")
        self.dvk.set_next_ids("ID2")
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last() == True
        self.dvk.set_previous_ids()
        assert self.dvk.get_section_last() == False
        
    def test_get_set_sequence_title(self):
        """
        Tests the get_sequence_title and set_sequence_title functions of the Dvk class.
        """
        #NO SEQUENCE DATA
        self.dvk.set_sequence_title("invalid")
        assert self.dvk.get_sequence_title() == ""
        #MISSING SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_sequence_title("still invalid")
        assert self.dvk.get_sequence_title() == ""
        self.dvk.set_previous_ids()
        self.dvk.set_next_ids(["ID2"])
        self.dvk.set_sequence_title("nope")
        assert self.dvk.get_sequence_title() == ""
        #FULL SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_sequence_title("finally")
        assert self.dvk.get_sequence_title() == "finally"
        #LAST/FIRST IN SEQUENCE
        self.dvk.set_previous_ids([])
        self.dvk.set_sequence_title("different")
        assert self.dvk.get_sequence_title() == "different"
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_next_ids([])
        self.dvk.set_sequence_title("other")
        assert self.dvk.get_sequence_title() == "other"
        #SINGLE
        self.dvk.set_previous_ids([])
        self.dvk.set_sequence_title("invalid again")
        assert self.dvk.get_sequence_title() == ""
        #INVALID AFTER SETTING
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_sequence_title("yep")
        assert self.dvk.get_sequence_title() == "yep"
        self.dvk.set_previous_ids([])
        assert self.dvk.get_sequence_title() == ""
        self.dvk.set_previous_ids("ID1")
        self.dvk.set_next_ids("ID2")
        self.dvk.set_sequence_title("yes")
        assert self.dvk.get_sequence_title() == "yes"
        self.dvk.set_previous_ids()
        assert self.dvk.get_sequence_title() == ""
    
    def test_get_set_section_title(self):
        """
        Tests the get_section_title and set_section_title functions of the Dvk class.
        """
        self.dvk.set_section_title("invalid")
        assert self.dvk.get_section_title() == ""
        #MISSING SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_title("still invalid")
        assert self.dvk.get_section_title() == ""
        self.dvk.set_previous_ids()
        self.dvk.set_next_ids(["ID2"])
        self.dvk.set_section_title("nope")
        assert self.dvk.get_section_title() == ""
        #FULL SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_title("finally")
        assert self.dvk.get_section_title() == "finally"
        #LAST/FIRST IN SEQUENCE
        self.dvk.set_previous_ids([])
        self.dvk.set_section_title("different")
        assert self.dvk.get_section_title() == "different"
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_next_ids([])
        self.dvk.set_section_title("other")
        assert self.dvk.get_section_title() == "other"
        #SINGLE
        self.dvk.set_previous_ids([])
        self.dvk.set_section_title("invalid again")
        assert self.dvk.get_section_title() == ""
        #INVALID AFTER SETTING
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_title("yep")
        assert self.dvk.get_section_title() == "yep"
        self.dvk.set_previous_ids([])
        assert self.dvk.get_section_title() == ""
        self.dvk.set_previous_ids("ID1")
        self.dvk.set_next_ids("ID2")
        self.dvk.set_section_title("yes")
        assert self.dvk.get_section_title() == "yes"
        self.dvk.set_previous_ids()
        assert self.dvk.get_section_title() == ""
        
    