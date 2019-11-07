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
        #DVK 1
        dvk = Dvk()
        dvk.set_file(self.test_dir.joinpath("dvk2.dvk").absolute())
        dvk.set_id("Unimportant")
        dvk.set_title("DVK 2")
        dvk.set_artists(["Guy", "Other Guy"])
        dvk.set_int_time(2019,11,2,12,0)
        dvk.set_page_url("/unimportant")
        dvk.set_media_file("unimportant")
        dvk.set_rating(5)
        dvk.set_views(128)
        dvk.write_dvk()
        #DVK 2
        dvk.set_int_time(2018,11,2,11,15)
        dvk.set_file(self.test_dir.joinpath("dvk2-2.dvk").absolute())
        dvk.set_rating(0)
        dvk.set_views(0)
        dvk.write_dvk()
        #DVK 3
        dvk.set_title("DVK 10")
        dvk.set_int_time(2019,11,2,11,15)
        dvk.set_file(self.test_dir.joinpath("dvk10.dvk").absolute())
        dvk.set_rating(4)
        dvk.set_views(7)
        dvk.write_dvk()
        #DVK 4
        dvk.set_title("DVK 5.25 - Fun!")
        dvk.set_artist("Artist")
        dvk.set_int_time(2019,5,2,5,25)
        dvk.set_file(self.test_dir.joinpath("dvk5-25.dvk").absolute())
        dvk.write_dvk()
        #DVK 5
        dvk.set_title("DVK 5 - Fun!")
        dvk.set_file(self.test_dir.joinpath("dvk5.dvk").absolute())
        dvk.set_rating(1)
        dvk.set_views(67)
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
        assert self.dvk_directory.get_size() == 5
        self.dvk_directory.read_dvks()
        assert self.dvk_directory.get_size() == 0
        
    def test_sort_dvks_alpha(self):
        """
        Tests alpha-numeric sorting with the sort_dvks function of the DvkDirectory class.
        """
        self.dvk_directory.sort_dvks("a")
        assert self.dvk_directory.get_size() == 5
        assert self.dvk_directory.get_dvk(0).get_title() == "DVK 2"
        assert self.dvk_directory.get_dvk(0).get_time() == "2018/11/02|11:15"
        assert self.dvk_directory.get_dvk(1).get_title() == "DVK 2"
        assert self.dvk_directory.get_dvk(1).get_time() == "2019/11/02|12:00"
        assert self.dvk_directory.get_dvk(2).get_title() == "DVK 5 - Fun!"
        assert self.dvk_directory.get_dvk(3).get_title() == "DVK 5.25 - Fun!"
        assert self.dvk_directory.get_dvk(4).get_title() == "DVK 10"
        
    def test_sort_dvks_time(self):
        """
        Tests sorting by time with the sort_dvks function of the DvkDirectory class.
        """
        self.dvk_directory.sort_dvks("t")
        assert self.dvk_directory.get_size() == 5
        assert self.dvk_directory.get_dvk(0).get_time() == "2018/11/02|11:15"
        assert self.dvk_directory.get_dvk(1).get_time() == "2019/05/02|05:25"
        assert self.dvk_directory.get_dvk(1).get_title() == "DVK 5 - Fun!"
        assert self.dvk_directory.get_dvk(2).get_time() == "2019/05/02|05:25"
        assert self.dvk_directory.get_dvk(2).get_title() == "DVK 5.25 - Fun!"
        assert self.dvk_directory.get_dvk(3).get_time() == "2019/11/02|11:15"
        assert self.dvk_directory.get_dvk(4).get_time() == "2019/11/02|12:00"
        
    def test_sort_dvks_ratings(self):
        """
        Tests sorting by ratings with the sort_dvks function of the DvkDirectory class.
        """
        self.dvk_directory.sort_dvks("r")
        assert self.dvk_directory.get_size() == 5
        assert self.dvk_directory.get_dvk(0).get_rating() == 0
        assert self.dvk_directory.get_dvk(1).get_rating() == 1
        assert self.dvk_directory.get_dvk(2).get_rating() == 4
        assert self.dvk_directory.get_dvk(2).get_title() == "DVK 5.25 - Fun!"
        assert self.dvk_directory.get_dvk(3).get_rating() == 4
        assert self.dvk_directory.get_dvk(3).get_title() == "DVK 10"
        assert self.dvk_directory.get_dvk(4).get_rating() == 5
        
    def test_sort_dvks_views(self):
        """
        Tests sorting by view count with the sort_dvks function of the DvkDirectory class.
        """
        self.dvk_directory.sort_dvks("v")
        assert self.dvk_directory.get_size() == 5
        assert self.dvk_directory.get_dvk(0).get_views() == 0
        assert self.dvk_directory.get_dvk(1).get_views() == 7
        assert self.dvk_directory.get_dvk(1).get_title() == "DVK 5.25 - Fun!"
        assert self.dvk_directory.get_dvk(2).get_views() == 7
        assert self.dvk_directory.get_dvk(2).get_title() == "DVK 10"
        assert self.dvk_directory.get_dvk(3).get_views() == 67
        assert self.dvk_directory.get_dvk(4).get_views() == 128
        