import unittest
from file.Dvk import Dvk
from file.DvkDirectory import DvkDirectory
from pathlib import Path
import shutil

class DvkDirectoryTest(unittest.TestCase):
    """
    Unit tests for the DvkDirectory class.
    
    Attributes:
        test_dir (Path): Directory for holding DVK files used in testing.
        dvk_directory (DvkDirectory):
    """
    
    def setUp(self):
        """
        Initializes DvkDirectoryTest attributes for testing.
        """
        unittest.TestCase.setUp(self)
        self.test_dir = Path("dirtest")
        self.test_dir.mkdir(exist_ok=True)
        dvk = Dvk()
        dvk.set_file(self.test_dir.joinpath("dvk1.dvk").absolute())
        dvk.set_id("Unimportant")
        dvk.set_title("DVK 2")
        dvk.set_artists(["Guy", "Other Guy"])
        dvk.set_int_time(2019,11,2,12,0)
        dvk.set_page_url("/unimportant")
        dvk.set_media_file("unimportant")
        dvk.write_dvk()
        dvk.set_title("DVK 10")
        dvk.set_int_time(2019,11,2,11,15)
        dvk.set_file(self.test_dir.joinpath("dvk10.dvk").absolute())
        dvk.write_dvk()
        dvk.set_title("DVK 5.25 - Fun!")
        dvk.set_artist("Artist")
        dvk.set_int_time(2019,5,2,5,25)
        dvk.set_file(self.test_dir.joinpath("dvk5-25.dvk").absolute())
        dvk.write_dvk()
        dvk.set_title("DVK 5 - Fun!")
        dvk.set_file(self.test_dir.joinpath("dvk5.dvk").absolute())
        dvk.write_dvk()
        self.dvk_directory = DvkDirectory()
        self.dvk_directory.read_dvks(self.test_dir.absolute())
    
    def tearDown(self):
        """
        Deletes test files after DvkDirectory testing.
        """
        unittest.TestCase.tearDown(self)
        shutil.rmtree(self.test_dir.absolute())
    
    def test_get_size(self):
        """
        Tests the get_size function of the DvkDirectory class.
        """
        assert self.dvk_directory.get_size() == 4
        self.dvk_directory.read_dvks()
        assert self.dvk_directory.get_size() == 0
        
    def test_sort_dvks(self):
        """
        Tests the sort_dvks function of the DvkDirectory class.
        """
        self.dvk_directory.sort_dvks()
        assert self.dvk_directory.get_size() == 4
        assert self.dvk_directory.get_dvk(0).get_title() == "DVK 2"
        assert self.dvk_directory.get_dvk(1).get_title() == "DVK 5 - Fun!"
        assert self.dvk_directory.get_dvk(2).get_title() == "DVK 5.25 - Fun!"
        assert self.dvk_directory.get_dvk(3).get_title() == "DVK 10"
        