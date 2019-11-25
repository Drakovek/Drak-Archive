import unittest
from pathlib import Path
from shutil import rmtree
from drak_archive.file.dvk import Dvk
from drak_archive.file.dvk_handler import DvkHandler
from drak_archive.error.error_finding import identical_ids
from drak_archive.error.error_finding import missing_media
from drak_archive.error.error_finding import unlinked_media


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
        self.test_dir.joinpath("file0").touch()
        sub = Path(self.test_dir.joinpath("sub").absolute())
        sub.mkdir(exist_ok=True)
        # DVK 1
        dvk = Dvk(self.test_dir.joinpath("dvk1.dvk").absolute())
        file = self.test_dir.joinpath("file1.txt")
        file.touch()
        dvk.set_id("id1")
        dvk.set_title("title1")
        dvk.set_artist("artist")
        dvk.set_page_url("/page/url")
        dvk.set_media_file(file)
        file = self.test_dir.joinpath("fileSecond.no")
        file.touch()
        dvk.set_secondary_file(file)
        dvk.write_dvk()
        # DVK 2
        file = sub.joinpath("file2.png")
        file.touch()
        dvk.set_id("id2")
        dvk.set_title("title2")
        dvk.set_file(sub.joinpath("dvk2.dvk").absolute())
        dvk.set_media_file(file)
        file = sub.joinpath("second.dmf")
        dvk.set_secondary_file(file)
        dvk.write_dvk()
        # DVK 3
        sub.joinpath("file1.txt").touch()
        file = sub.joinpath("file3.svg")
        dvk.set_id("id1")
        dvk.set_title("title3")
        dvk.set_file(sub.joinpath("dvk3.dvk").absolute())
        dvk.set_media_file(file)
        dvk.set_secondary_file(None)
        dvk.write_dvk()
        # DVK 4
        file = self.test_dir.joinpath("file4.ogg")
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
        assert identical_ids([sub.absolute()]) == []
        assert identical_ids() == []
        assert len(identical_ids([self.test_dir.absolute()])) == 3

    def test_missing_media(self):
        """
        Tests the missing_media function.
        """
        handler = DvkHandler()
        handler.load_dvks([self.test_dir.absolute()])
        missing = missing_media(dvk_handler=handler)
        assert len(missing) == 3
        assert missing[0].name == "dvk2.dvk"
        assert missing[1].name == "dvk3.dvk"
        assert missing[2].name == "dvk4.dvk"
        assert missing_media() == []
        sub = Path(self.test_dir.joinpath("sub").absolute())
        missing = missing_media([sub.absolute()])
        assert len(missing) == 2
        assert missing[0].name == "dvk2.dvk"
        assert missing[1].name == "dvk3.dvk"

    def test_unlinked_media(self):
        """
        Tests the unlinked_media function.
        """
        missing = unlinked_media([self.test_dir.absolute()])
        assert len(missing) == 2
        assert missing[0].name == "file0"
        assert missing[1].name == "file1.txt"
        assert unlinked_media() == []
        handler = DvkHandler()
        handler.load_dvks([self.test_dir.joinpath("sub").absolute()])
        missing = unlinked_media(dvk_handler=handler)
        assert len(missing) == 1
        assert missing[0].name == "file1.txt"
