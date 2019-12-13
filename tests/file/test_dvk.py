import unittest
from json import dump
from os import listdir, remove, stat
from pathlib import Path
from shutil import rmtree
from dvk_archive.file.dvk import Dvk


class TestDvk(unittest.TestCase):
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
        # CHECK EMPTY
        assert self.dvk.get_title() is None
        assert self.dvk.get_id() == ""
        assert self.dvk.get_title() is None
        assert self.dvk.get_artists() == []
        assert self.dvk.get_time() == "0000/00/00|00:00"
        assert self.dvk.get_web_tags() is None
        assert self.dvk.get_description() is None
        assert self.dvk.get_page_url() is None
        assert self.dvk.get_direct_url() is None
        assert self.dvk.get_secondary_url() is None
        assert self.dvk.get_media_file() is None
        assert self.dvk.get_secondary_file() is None
        assert self.dvk.get_previous_ids() is None
        assert self.dvk.get_next_ids() is None
        assert not self.dvk.get_section_first()
        assert not self.dvk.get_section_last()
        assert self.dvk.get_sequence_title() is None
        assert self.dvk.get_section_title() is None
        assert self.dvk.get_branch_titles() is None
        assert self.dvk.rating == 0
        assert self.dvk.views == 0
        assert self.dvk.user_tags is None
        # GET FILENAME
        file_path = Path("writeTest.dvk").absolute()
        # SET DVK DATA
        self.dvk.set_id("id702")
        self.dvk.set_title("ConstructorTestTitle")
        self.dvk.set_artist("artistName")
        self.dvk.set_page_url("/url/")
        self.dvk.set_file(file_path)
        self.dvk.set_media_file("media.jpg")
        self.dvk.write_dvk()
        # CHECK VALUES
        loaded_dvk = Dvk(file_path)
        assert loaded_dvk.get_id() == "ID702"
        assert loaded_dvk.get_title() == "ConstructorTestTitle"
        assert loaded_dvk.get_artists()[0] == "artistName"
        assert loaded_dvk.get_page_url() == "/url/"
        assert loaded_dvk.get_media_file().name == "media.jpg"
        remove(file_path)

    def test_read_write_dvk(self):
        """
        Tests the read_dvk and write_dvk functions.
        """
        # GET FILENAME
        file_path = Path("writeTest.dvk").absolute()
        # SET DVK DATA
        self.dvk.set_file(file_path)
        self.dvk.set_id("id1234")
        self.dvk.set_title("WriteTestTitle")
        self.dvk.set_artists(["artist", "other artist"])
        self.dvk.set_time_int(1864, 10, 31, 7, 2)
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
        self.dvk.set_branch_titles(["branch 1", "Branch 2"])
        self.dvk.set_rating(4)
        self.dvk.set_views(15)
        self.dvk.set_user_tags(["some", "Tags"])
        # WRITE THEN READ
        self.dvk.write_dvk()
        self.dvk.read_dvk()
        remove(file_path)
        # CHECK VALUES
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
        assert self.dvk.get_section_first()
        assert self.dvk.get_section_last()
        assert self.dvk.get_sequence_title() == "Seq Title"
        assert self.dvk.get_section_title() == "Section"
        assert self.dvk.get_branch_titles()[0] == "branch 1"
        assert self.dvk.get_branch_titles()[1] == "Branch 2"
        assert self.dvk.get_rating() == 4
        assert self.dvk.get_views() == 15
        assert self.dvk.get_user_tags()[0] == "some"
        assert self.dvk.get_user_tags()[1] == "Tags"
        # CHECK SEQUENCE WRITING
        self.dvk.set_previous_ids(None)
        self.dvk.set_next_ids(None)
        self.dvk.write_dvk()
        self.dvk.read_dvk()
        assert self.dvk.get_previous_ids() is None
        assert self.dvk.get_next_ids() is None
        self.dvk.set_previous_ids([])
        self.dvk.set_next_ids([])
        self.dvk.write_dvk()
        self.dvk.read_dvk()
        assert self.dvk.get_previous_ids() == []
        assert self.dvk.get_next_ids() == []
        # CHECK READING NON-EXISTANT FILE
        self.dvk.set_file(None)
        self.dvk.read_dvk()
        assert self.dvk.get_title() is None
        # CHECK READING INVALID FILE
        data = {"test": "nope"}
        try:
            with open(file_path, "w") as out_file:
                dump(data, out_file)
        except IOError as e:
            print("File error: " + str(e))
        self.dvk.read_dvk()
        remove(file_path)
        assert self.dvk.get_title() is None
        # CHECK WRITING INVALID FILE
        invalid_dvk = Dvk()
        invalid_path = Path("nonExistant.dvk")
        invalid_dvk.set_file(invalid_path.absolute())
        assert not invalid_path.exists()

    def test_write_media(self):
        """
        Tests the write_media function.
        """
        test_dir = Path("renameTest")
        test_dir.mkdir(exist_ok=True)
        try:
            # INVALID DVK
            dvk = Dvk()
            dvk.set_id("ID123")
            dvk.set_title("Title")
            dvk.set_artist("Artist")
            dvk.set_file(test_dir.joinpath("dvk1.dvk"))
            dvk.set_media_file("media.jpg")
            dvk.set_direct_url("kjlmlwonluyhj")
            dvk.write_media()
            assert listdir(str(test_dir.absolute())) == []
            # INVALID DIRECT URL
            dvk.set_page_url("/whatever")
            dvk.write_media()
            assert listdir(str(test_dir.absolute())) == []
            # VALID MEDIA
            url = "http://www.pythonscraping.com/img/gifts/img6.jpg"
            dvk.set_direct_url(url)
            dvk.write_media()
            assert dvk.get_time() == "0000/00/00|00:00"
            assert dvk.get_file().exists()
            assert dvk.get_media_file().exists()
            assert stat(str(dvk.get_media_file().absolute())).st_size == 39785
            remove(str(dvk.get_file().absolute()))
            remove(str(dvk.get_media_file().absolute()))
            # INVALID SECONDARY URL
            dvk.set_secondary_file("second.jpg")
            dvk.set_secondary_url("lksjamelkwelkmwm")
            dvk.write_media()
            assert listdir(str(test_dir.absolute())) == []
            # VALID DIRECT AND SECONDARY URLS
            dvk.set_secondary_url(url)
            dvk.write_media(True)
            assert dvk.get_time() == "2014/08/04|00:49"
            assert dvk.get_file().exists()
            assert dvk.get_media_file().exists()
            assert dvk.get_secondary_file().exists()
            assert stat(str(dvk.get_media_file().absolute())).st_size == 39785
            filename = str(dvk.get_secondary_file().absolute())
            assert stat(filename).st_size == 39785
        finally:
            # DELETE TEST FILES
            rmtree(test_dir.absolute())

    def test_add_to_dict(self):
        """
        Tests the add_to_dict function.
        """
        start_dict = dict()
        end_dict = self.dvk.add_to_dict()
        assert end_dict is None
        end_dict = self.dvk.add_to_dict(start_dict)
        assert start_dict == end_dict
        end_dict = self.dvk.add_to_dict(start_dict, "key")
        assert start_dict == end_dict
        end_dict = self.dvk.add_to_dict(start_dict, None, "temp")
        assert start_dict == end_dict
        start_dict = self.dvk.add_to_dict(start_dict, "key", "string")
        assert self.dvk.get_from_dict(start_dict, ["key"]) == "string"
        start_dict = self.dvk.add_to_dict(start_dict, "other", 5)
        assert self.dvk.get_from_dict(start_dict, ["other"]) == 5

    def test_get_from_dict(self):
        """
        Tests the get_from_dict function.
        """
        int_dict = dict()
        int_dict["thing"] = "blah"
        dictionary = dict()
        dictionary["key"] = "Yes"
        dictionary["internal"] = int_dict
        assert self.dvk.get_from_dict() is None
        assert self.dvk.get_from_dict(dictionary, None, None) is None
        assert self.dvk.get_from_dict(None, ["key"], "fallback") == "fallback"
        assert self.dvk.get_from_dict(dictionary, ["key"]) == "Yes"
        keys = ["internal", "thing"]
        assert self.dvk.get_from_dict(dictionary, keys) == "blah"
        keys = ["internal", "no_key"]
        assert self.dvk.get_from_dict(dictionary, keys) is None

    def test_can_write(self):
        """
        Tests the can_write function.
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

    def test_get_filename(self):
        """
        Tests the get_filename function.
        """
        assert self.dvk.get_filename() == ""
        self.dvk.set_title("Title")
        assert self.dvk.get_filename() == ""
        self.dvk.set_id("ID123")
        self.dvk.set_title(None)
        assert self.dvk.get_filename() == ""
        self.dvk.set_title("Yay  more-files!")
        assert self.dvk.get_filename() == "Yay more-files_ID123"
        self.dvk.set_title("")
        assert self.dvk.get_filename() == "0_ID123"

    def test_rename_files(self):
        """
        Tests the rename_files function.
        """
        test_dir = Path("renameTest")
        test_dir.mkdir(exist_ok=True)
        dvk = Dvk()
        dvk.set_file(test_dir.joinpath("dvk1.dvk").absolute())
        dvk.set_id("DVK1234")
        dvk.set_title("Yay DVK!")
        dvk.set_artist("Me")
        dvk.set_page_url("/test")
        dvk.set_media_file("file.txt")
        dvk.set_secondary_file("second.png")
        dvk.get_media_file().touch()
        dvk.get_secondary_file().touch()
        dvk.write_dvk()
        dvk.rename_files()
        assert dvk.get_file().name == "Yay DVK_DVK1234.dvk"
        assert dvk.get_file().exists()
        assert dvk.get_media_file().name == "Yay DVK_DVK1234.txt"
        assert dvk.get_media_file().exists()
        assert dvk.get_secondary_file().name == "Yay DVK_DVK1234.png"
        assert dvk.get_secondary_file().exists()
        # CHECK SPECIFIC NAME
        dvk.rename_files("different")
        assert dvk.get_file().name == "different.dvk"
        assert dvk.get_file().exists()
        assert dvk.get_media_file().name == "different.txt"
        assert dvk.get_media_file().exists()
        assert dvk.get_secondary_file().name == "different.png"
        assert dvk.get_secondary_file().exists()
        # CHECK NO SECONDARY
        dvk.set_title("No Sec")
        dvk.set_secondary_file("Bleh")
        dvk.write_dvk()
        dvk.rename_files()
        dvk.set_secondary_file(None)
        dvk.write_dvk()
        dvk.rename_files()
        assert dvk.get_file().name == "No Sec_DVK1234.dvk"
        assert dvk.get_file().exists()
        assert dvk.get_media_file().name == "No Sec_DVK1234.txt"
        assert dvk.get_media_file().exists()
        # CHECK NO MEDIA
        dvk.set_title("No Med")
        dvk.set_media_file("nonexistant.png")
        dvk.write_dvk()
        dvk.rename_files()
        dvk.set_media_file(None)
        dvk.rename_files()
        assert dvk.get_file().name == "No Med_DVK1234.dvk"
        assert dvk.get_file().exists()
        # DELETE TEST FILES
        rmtree(test_dir.absolute())

    def test_get_set_file(self):
        """
        Tests the get_file and set_file functions.
        """
        self.dvk.set_file()
        assert self.dvk.get_file() is None
        self.dvk.set_file(None)
        assert self.dvk.get_file() is None
        self.dvk.set_file("")
        assert self.dvk.get_file() is None
        self.dvk.set_file("test_path.dvk")
        assert self.dvk.get_file().name == "test_path.dvk"

    def test_generate_id(self):
        """
        Tests the generate_id function.
        """
        self.dvk.generate_id("DVK")
        assert self.dvk.get_id() == ""
        self.dvk.set_title("Title1")
        self.dvk.generate_id()
        assert self.dvk.get_id() == ""
        self.dvk.set_artist("artist")
        self.dvk.set_page_url("/url")
        self.dvk.generate_id()
        assert self.dvk.get_id() == "4309082618"
        self.dvk.generate_id("VGK")
        assert self.dvk.get_id() == "VGK4309082618"
        self.dvk.generate_id("VGK", extra="bleh")
        assert self.dvk.get_id() == "VGK9821911274"
        self.dvk.set_title("Title2")
        self.dvk.generate_id("DVK")
        assert self.dvk.get_id() == "DVK9413915306"

    def test_get_set_id(self):
        """
        Tests the get_id and set_id functions.
        """
        self.dvk.set_id()
        assert self.dvk.get_id() == ""
        self.dvk.set_id(None)
        assert self.dvk.get_id() == ""
        self.dvk.set_id("id123")
        assert self.dvk.get_id() == "ID123"

    def test_get_set_title(self):
        """
        Tests the get_title and set_title functions.
        """
        self.dvk.set_title()
        assert self.dvk.get_title() is None
        self.dvk.set_title(None)
        assert self.dvk.get_title() is None
        self.dvk.set_title("")
        assert self.dvk.get_title() == ""
        self.dvk.set_title("TestTitle")
        assert self.dvk.get_title() == "TestTitle"

    def test_get_set_artists(self):
        """
        Tests the get_artists, set_artists, and set_artist functions.
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
        ats = []
        ats.append("artist10")
        ats.append("artist10")
        ats.append("")
        ats.append(None)
        ats.append("artist1")
        ats.append("test10.0.20-stuff")
        ats.append("test10.0.0-stuff")
        self.dvk.set_artists(ats)
        assert len(self.dvk.get_artists()) == 4
        assert self.dvk.get_artists()[0] == "artist1"
        assert self.dvk.get_artists()[1] == "artist10"
        assert self.dvk.get_artists()[2] == "test10.0.0-stuff"
        assert self.dvk.get_artists()[3] == "test10.0.20-stuff"

    def test_set_int_time(self):
        """
        Tests the set_int_time function.
        """
        self.dvk.set_time_int()
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_time_int(None, None, None, None, None)
        assert self.dvk.get_time() == "0000/00/00|00:00"

        # TEST INVALID YEAR
        self.dvk.set_time_int(0, 10, 10, 7, 15)
        assert self.dvk.get_time() == "0000/00/00|00:00"

        # TEST INVALID MONTH
        self.dvk.set_time_int(2017, 0, 10, 7, 15)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_time_int(2017, 13, 10, 7, 15)
        assert self.dvk.get_time() == "0000/00/00|00:00"

        # TEST INVALID DAY
        self.dvk.set_time_int(2017, 10, 0, 7, 15)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_time_int(2017, 10, 32, 7, 15)
        assert self.dvk.get_time() == "0000/00/00|00:00"

        # TEST INVALID HOUR
        self.dvk.set_time_int(2017, 10, 10, -1, 0)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_time_int(2017, 10, 10, 24, 0)
        assert self.dvk.get_time() == "0000/00/00|00:00"

        # TEST INVALID MINUTE
        self.dvk.set_time_int(2017, 10, 10, 7, -1)
        assert self.dvk.get_time() == "0000/00/00|00:00"
        self.dvk.set_time_int(2017, 10, 10, 7, 60)
        assert self.dvk.get_time() == "0000/00/00|00:00"

        # TEST VALID TIME
        self.dvk.set_time_int(2017, 10, 10, 7, 0)
        assert self.dvk.get_time() == "2017/10/10|07:00"

    def test_get_set_time(self):
        """
        Tests the get_time and set_time functions.
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
        Tests the get_web_tags and set_web_tags functions.
        """
        self.dvk.set_web_tags()
        assert self.dvk.get_web_tags() is None
        self.dvk.set_web_tags(None)
        assert self.dvk.get_web_tags() is None
        self.dvk.set_web_tags([])
        assert self.dvk.get_web_tags() is None
        self.dvk.set_web_tags(["tag1", "Tag2", "other tag", "tag1", None, ""])
        assert len(self.dvk.get_web_tags()) == 3
        assert self.dvk.get_web_tags()[0] == "tag1"
        assert self.dvk.get_web_tags()[1] == "Tag2"
        assert self.dvk.get_web_tags()[2] == "other tag"

    def test_get_set_description(self):
        """
        Tests the get_description and set_description functions.
        """
        self.dvk.set_description()
        assert self.dvk.get_description() is None
        self.dvk.set_description(None)
        assert self.dvk.get_description() is None
        self.dvk.set_description("")
        assert self.dvk.get_description() is None
        self.dvk.set_description("<i>Baño</i>")
        assert self.dvk.get_description() == "<i>Ba&#241;o</i>"

    def test_get_set_page_url(self):
        """
        Tests the get_page_url and set_page_url functions.
        """
        self.dvk.set_page_url()
        assert self.dvk.get_page_url() is None
        self.dvk.set_page_url(None)
        assert self.dvk.get_page_url() is None
        self.dvk.set_page_url("")
        assert self.dvk.get_page_url() is None
        self.dvk.set_page_url("/Page/url")
        assert self.dvk.get_page_url() == "/Page/url"

    def test_get_set_direct_url(self):
        """
        Tests the get_direct_url and set_direct_url functions.
        """
        self.dvk.set_direct_url()
        assert self.dvk.get_direct_url() is None
        self.dvk.set_direct_url(None)
        assert self.dvk.get_direct_url() is None
        self.dvk.set_direct_url("")
        assert self.dvk.get_direct_url() is None
        self.dvk.set_direct_url("/direct/URL")
        assert self.dvk.get_direct_url() == "/direct/URL"

    def test_get_set_secondary_url(self):
        """
        Tests the get_secondary_url and set_secondary_url functions.
        """
        self.dvk.set_secondary_url()
        assert self.dvk.get_secondary_url() is None
        self.dvk.set_secondary_url(None)
        assert self.dvk.get_secondary_url() is None
        self.dvk.set_secondary_url("")
        assert self.dvk.get_secondary_url() is None
        self.dvk.set_secondary_url("/Secondary/Url")
        assert self.dvk.get_secondary_url() == "/Secondary/Url"

    def test_get_set_media_file(self):
        """
        Tests the get_media_file and set_media_file functions.
        """
        self.dvk.set_media_file("bleh.png")
        assert self.dvk.get_media_file() is None
        self.dvk.set_file(Path("media.dvk").absolute())
        self.dvk.set_media_file("media.png")
        assert self.dvk.get_media_file().name == "media.png"
        assert self.dvk.get_file().parent == self.dvk.get_media_file().parent
        self.dvk.set_media_file()
        assert self.dvk.get_media_file() is None
        self.dvk.set_media_file(None)
        assert self.dvk.get_media_file() is None
        self.dvk.set_media_file("")
        assert self.dvk.get_media_file() is None

    def test_get_set_secondary_file(self):
        """
        Tests the get_secondary_file and set_secondary_file functions.
        """
        self.dvk.set_secondary_file("other.png")
        assert self.dvk.get_media_file() is None
        self.dvk.set_file(Path("mine.dvk").absolute())
        self.dvk.set_secondary_file("second.png")
        assert self.dvk.get_secondary_file().name == "second.png"
        value = self.dvk.get_secondary_file().parent
        assert self.dvk.get_file().parent == value
        self.dvk.set_secondary_file()
        assert self.dvk.get_secondary_file() is None
        self.dvk.set_secondary_file("")
        assert self.dvk.get_secondary_file() is None
        self.dvk.set_secondary_file(None)
        assert self.dvk.get_secondary_file() is None

    def test_get_set_previous_ids(self):
        """
        Tests the get_previous_ids and set_previous_ids functions.
        """
        self.dvk.set_previous_ids()
        assert self.dvk.get_previous_ids() is None
        self.dvk.set_previous_ids(None)
        assert self.dvk.get_previous_ids() is None
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
        Tests the get_next_ids and set_next_ids functions.
        """
        self.dvk.set_next_ids()
        assert self.dvk.get_next_ids() is None
        self.dvk.set_next_ids(None)
        assert self.dvk.get_next_ids() is None
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
        Tests the get_section_first and set_section_first functions.
        """
        self.dvk.set_section_first(True)
        assert not self.dvk.get_section_first()
        # MISSING SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_first(True)
        assert not self.dvk.get_section_first()
        self.dvk.set_previous_ids()
        self.dvk.set_next_ids(["ID2"])
        self.dvk.set_section_first(True)
        assert not self.dvk.get_section_first()
        # FULL SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first()
        # LAST/FIRST IN SEQUENCE
        self.dvk.set_previous_ids([])
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first()
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_next_ids([])
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first()
        # SINGLE
        self.dvk.set_previous_ids([])
        self.dvk.set_section_first(True)
        assert not self.dvk.get_section_first()
        # INVALID AFTER SETTING
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first()
        self.dvk.set_previous_ids([])
        assert not self.dvk.get_section_first()
        self.dvk.set_previous_ids("ID1")
        self.dvk.set_next_ids("ID2")
        self.dvk.set_section_first(True)
        assert self.dvk.get_section_first()
        self.dvk.set_previous_ids()
        assert not self.dvk.get_section_first()

    def test_get_set_section_last(self):
        """
        Tests the get_section_last and set_section_last functions.
        """
        self.dvk.set_section_last(True)
        assert not self.dvk.get_section_last()
        # MISSING SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_last(True)
        assert not self.dvk.get_section_last()
        self.dvk.set_previous_ids()
        self.dvk.set_next_ids(["ID2"])
        self.dvk.set_section_last(True)
        assert not self.dvk.get_section_last()
        # FULL SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last()
        # LAST/FIRST IN SEQUENCE
        self.dvk.set_previous_ids([])
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last()
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_next_ids([])
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last()
        # SINGLE
        self.dvk.set_previous_ids([])
        self.dvk.set_section_last(True)
        assert not self.dvk.get_section_last()
        # INVALID AFTER SETTING
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last()
        self.dvk.set_previous_ids([])
        assert not self.dvk.get_section_last()
        self.dvk.set_previous_ids("ID1")
        self.dvk.set_next_ids("ID2")
        self.dvk.set_section_last(True)
        assert self.dvk.get_section_last()
        self.dvk.set_previous_ids()
        assert not self.dvk.get_section_last()

    def test_get_set_sequence_title(self):
        """
        Tests the get_sequence_title and set_sequence_title functions.
        """
        # NO SEQUENCE DATA
        self.dvk.set_sequence_title("invalid")
        assert self.dvk.get_sequence_title() is None
        # MISSING SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_sequence_title("still invalid")
        assert self.dvk.get_sequence_title() is None
        self.dvk.set_previous_ids()
        self.dvk.set_next_ids(["ID2"])
        self.dvk.set_sequence_title("nope")
        assert self.dvk.get_sequence_title() is None
        # FULL SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_sequence_title("finally")
        assert self.dvk.get_sequence_title() == "finally"
        # LAST/FIRST IN SEQUENCE
        self.dvk.set_previous_ids([])
        self.dvk.set_sequence_title("different")
        assert self.dvk.get_sequence_title() == "different"
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_next_ids([])
        self.dvk.set_sequence_title("other")
        assert self.dvk.get_sequence_title() == "other"
        self.dvk.set_sequence_title("")
        assert self.dvk.get_sequence_title() is None
        # SINGLE
        self.dvk.set_previous_ids([])
        self.dvk.set_sequence_title("invalid again")
        assert self.dvk.get_sequence_title() is None
        # INVALID AFTER SETTING
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_sequence_title("yep")
        assert self.dvk.get_sequence_title() == "yep"
        self.dvk.set_previous_ids([])
        assert self.dvk.get_sequence_title() is None
        self.dvk.set_previous_ids("ID1")
        self.dvk.set_next_ids("ID2")
        self.dvk.set_sequence_title("yes")
        assert self.dvk.get_sequence_title() == "yes"
        self.dvk.set_previous_ids()
        assert self.dvk.get_sequence_title() is None

    def test_get_set_section_title(self):
        """
        Tests the get_section_title and set_section_title functions.
        """
        self.dvk.set_section_title("invalid")
        assert self.dvk.get_section_title() is None
        # MISSING SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_title("still invalid")
        assert self.dvk.get_section_title() is None
        self.dvk.set_previous_ids()
        self.dvk.set_next_ids(["ID2"])
        self.dvk.set_section_title("nope")
        assert self.dvk.get_section_title() is None
        # FULL SEQUENCE DATA
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_title("finally")
        assert self.dvk.get_section_title() == "finally"
        self.dvk.set_section_title("")
        assert self.dvk.get_section_title() is None
        # LAST/FIRST IN SEQUENCE
        self.dvk.set_previous_ids([])
        self.dvk.set_section_title("different")
        assert self.dvk.get_section_title() == "different"
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_next_ids([])
        self.dvk.set_section_title("other")
        assert self.dvk.get_section_title() == "other"
        # SINGLE
        self.dvk.set_previous_ids([])
        self.dvk.set_section_title("invalid again")
        assert self.dvk.get_section_title() is None
        # INVALID AFTER SETTING
        self.dvk.set_previous_ids(["ID1"])
        self.dvk.set_section_title("yep")
        assert self.dvk.get_section_title() == "yep"
        self.dvk.set_previous_ids([])
        assert self.dvk.get_section_title() is None
        self.dvk.set_previous_ids("ID1")
        self.dvk.set_next_ids("ID2")
        self.dvk.set_section_title("yes")
        assert self.dvk.get_section_title() == "yes"
        self.dvk.set_previous_ids()
        assert self.dvk.get_section_title() is None

    def test_get_set_branch_titles(self):
        """
        Tests the get_branch_titles and set_branch_titles functions.
        """
        self.dvk.set_branch_titles(["invalid1", "invalid2"])
        assert self.dvk.get_branch_titles() is None
        self.dvk.set_next_ids(["ID1"])
        self.dvk.set_branch_titles(["not enough"])
        assert self.dvk.get_branch_titles() is None
        self.dvk.set_next_ids(["ID1", "ID2", "ID3"])
        self.dvk.set_branch_titles(["still", "not enough"])
        assert self.dvk.get_branch_titles() is None
        self.dvk.set_branch_titles(["This", "should", "work"])
        assert len(self.dvk.get_branch_titles()) == 3
        assert self.dvk.get_branch_titles()[0] == "This"
        assert self.dvk.get_branch_titles()[1] == "should"
        assert self.dvk.get_branch_titles()[2] == "work"
        self.dvk.set_branch_titles([])
        assert self.dvk.get_branch_titles() is None

    def test_get_set_rating(self):
        """
        Tests the get_rating and set_rating the Dvk class.
        """
        self.dvk.set_rating()
        assert self.dvk.get_rating() == 0
        self.dvk.set_rating(None)
        assert self.dvk.get_rating() == 0
        self.dvk.set_rating(-1)
        assert self.dvk.get_rating() == 0
        self.dvk.set_rating(6)
        assert self.dvk.get_rating() == 0
        self.dvk.set_rating(1)
        assert self.dvk.get_rating() == 1
        self.dvk.set_rating(5)
        assert self.dvk.get_rating() == 5
        self.dvk.set_rating(3)
        assert self.dvk.get_rating() == 3

    def test_get_set_views(self):
        """
        Tests the get_views and set_views functions.
        """
        self.dvk.set_views()
        assert self.dvk.get_views() == 0
        self.dvk.set_views(None)
        assert self.dvk.get_views() == 0
        self.dvk.set_views(-1)
        assert self.dvk.get_views() == 0
        self.dvk.set_views(128)
        assert self.dvk.get_views() == 128
        self.dvk.set_views(1)
        assert self.dvk.get_views() == 1

    def test_get_set_user_tags(self):
        """
        Tests the get_user_tags and set_user_tags functions.
        """
        self.dvk.set_user_tags()
        assert self.dvk.get_user_tags() is None
        self.dvk.set_user_tags(None)
        assert self.dvk.get_user_tags() is None
        self.dvk.set_user_tags([])
        assert self.dvk.get_user_tags() is None
        self.dvk.set_user_tags(["tag1", "Tag2", "other tag", "tag1", None, ""])
        assert len(self.dvk.get_user_tags()) == 3
        assert self.dvk.get_user_tags()[0] == "tag1"
        assert self.dvk.get_user_tags()[1] == "Tag2"
        assert self.dvk.get_user_tags()[2] == "other tag"
