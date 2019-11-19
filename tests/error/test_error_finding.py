import unittest
from pathlib import Path
from shutil import rmtree
from drak_archive.file.dvk import Dvk
from drak_archive.file.dvk_handler import DvkHandler
from drak_archive.error.error_finding import identical_ids


class TestErrorFinding(unittest.TestCase):
    """
    Unit tests for the ErrorFinding.py module.

    Attributes:
        test_dir (Path): Directory for holding test files.
    """

    def setUp(self):
        """
        Sets up test files before running unit tests.
        """
        unittest.TestCase.setUp(self)
        self.test_dir = Path("finding")
        self.test_dir.mkdir(exist_ok=True)
        sub = Path(self.test_dir.joinpath("sub").absolute())
        sub.mkdir(exist_ok=True)
        dvk = Dvk(self.test_dir.joinpath("dvk1.dvk").absolute())
        file = self.test_dir.joinpath("file1.txt")
        # DVK 1
        dvk.set_id("id1")
        dvk.set_title("title1")
        dvk.set_artist("artist")
        dvk.set_page_url("/page/url")
        dvk.set_media_file(file)
        dvk.write_dvk()
        # DVK 2
        file = sub.joinpath("file2.txt")
        dvk.set_id("id2")
        dvk.set_title("title2")
        dvk.set_file(sub.joinpath("dvk2.dvk").absolute())
        dvk.set_media_file(file)
        dvk.write_dvk()
        # DVK 3
        file = sub.joinpath("file3.txt")
        dvk.set_id("id1")
        dvk.set_title("title3")
        dvk.set_file(sub.joinpath("dvk3.dvk").absolute())
        dvk.set_media_file(file)
        dvk.write_dvk()
        # DVK 4
        file = self.test_dir.joinpath("file4.txt")
        dvk.set_title("title4")
        dvk.set_file(self.test_dir.joinpath("dvk4.dvk").absolute())
        dvk.set_media_file(file)
        dvk.write_dvk()

    def tearDown(self):
        """
        Deletes test files after ErrorFinding testing.
        """
        unittest.TestCase.tearDown(self)
        rmtree(self.test_dir.absolute())

    def test_identical_ids(self):
        """
        Tests the identical_ids function.
        """
        handler = DvkHandler()
        handler.load_dvks([self.test_dir.absolute()])
        ids = identical_ids(dvk_handler=handler)
        assert len(ids) == 3
        assert ids[0].name == "dvk1.dvk"
        assert ids[1].name == "dvk3.dvk"
        assert ids[2].name == "dvk4.dvk"
        sub = Path(self.test_dir.joinpath("sub").absolute())
        assert identical_ids(sub) == []
        assert identical_ids() == []
        assert len(identical_ids(self.test_dir.absolute())) == 3
