
import unittest
from pathlib import Path
from shutil import rmtree
from drak_archive.file.dvk import Dvk
from drak_archive.file.dvk_directory import DvkDirectory


class TestDvkDirectory(unittest.TestCase):
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
        # DVK 1
        dvk = Dvk()
        dvk.set_file(self.test_dir.joinpath("dvk2.dvk").absolute())
        dvk.set_id("Unimportant")
        dvk.set_title("DVK 2")
        dvk.set_artists(["Guy", "Other Guy"])
        dvk.set_time_int(2019, 11, 2, 12, 0)
        dvk.set_page_url("/unimportant")
        dvk.set_media_file("unimportant")
        dvk.set_rating(5)
        dvk.set_views(128)
        dvk.write_dvk()
        # DVK 2
        dvk.set_time_int(2018, 11, 2, 11, 15)
        dvk.set_file(self.test_dir.joinpath("dvk2-2.dvk").absolute())
        dvk.set_rating(0)
        dvk.set_views(0)
        dvk.write_dvk()
        # DVK 3
        dvk.set_title("DVK 10")
        dvk.set_artist("Guy")
        dvk.set_time_int(2019, 11, 2, 11, 15)
        dvk.set_file(self.test_dir.joinpath("dvk10.dvk").absolute())
        dvk.set_rating(4)
        dvk.set_views(7)
        dvk.write_dvk()
        # DVK 4
        dvk.set_title("DVK 5.25 - Fun!")
        dvk.set_artist("Artist")
        dvk.set_time_int(2019, 5, 2, 5, 25)
        dvk.set_file(self.test_dir.joinpath("dvk5-25.dvk").absolute())
        dvk.write_dvk()
        # DVK 5
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
        rmtree(self.test_dir.absolute())

    def test_get_size(self):
        """
        Tests the get_size function.
        """
        assert self.dvk_directory.get_size() == 5
        self.dvk_directory.read_dvks()
        assert self.dvk_directory.get_size() == 0
