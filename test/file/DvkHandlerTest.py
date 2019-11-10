import unittest
from shutil import rmtree
from pathlib import Path
from file.Dvk import Dvk
from file.DvkHandler import DvkHandler

class DvkHandlerTest(unittest.TestCase):
    """
    Unit tests for the DvkHandler class.
    
    Attributes:
        test_dir (Path): Directory for holding test files.
    """
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.test_dir = Path("handlerTest")
        self.test_dir.mkdir(exist_ok=True)
        dvk = Dvk()
        dvk.set_file(self.test_dir.joinpath("dvk.dvk").absolute())
        dvk.set_id("Unimportant")
        dvk.set_page_url("/unimportant")
        dvk.set_media_file("unimportant")
        count = 0
        while count < 2:
            dvk.set_file(self.test_dir.joinpath("dvk" + str(count) + ".dvk").absolute())
            dvk.set_title("DVK " + str(count))
            dvk.set_artist("Thing")
            dvk.set_int_time(2019,11,8,12,count)
            dvk.set_rating(count)
            dvk.set_views(count)
            dvk.write_dvk()
            count = count + 1
        #SUB-DIRECTORY 1
        sub1 = Path(self.test_dir.joinpath("sub1").absolute())
        sub1.mkdir(exist_ok=True)
        while count < 4:
            dvk.set_file(sub1.joinpath("dvk" + str(count) + ".dvk").absolute())
            dvk.set_title("DVK " + str(count))
            dvk.set_artist("Artist" + str(count))
            dvk.set_int_time(2019,11,8,12,count)
            dvk.set_rating(count)
            dvk.set_views(count)
            dvk.write_dvk()
            count = count + 1
        #SUB-DIRECTORY 2
        sub2 = Path(self.test_dir.joinpath("sub2").absolute())
        sub2.mkdir(exist_ok=True)
        while count < 6:
            dvk.set_file(sub2.joinpath("dvk" + str(count) + ".dvk").absolute())
            dvk.set_title("DVK " + str(count))
            dvk.set_artist("Thing")
            dvk.set_int_time(2019,11,8,12,count)
            dvk.set_rating(count)
            dvk.set_views(count)
            dvk.write_dvk()
            count = count + 1
        #INTERNAL SUB-DIRECTORY
        int_sub = Path(sub2.joinpath("intSub").absolute())
        int_sub.mkdir(exist_ok=True)
        while count < 8:
            dvk.set_file(int_sub.joinpath("dvk" + str(count) + ".dvk").absolute())
            dvk.set_title("DVK " + str(count))
            dvk.set_artist("Thing")
            dvk.set_int_time(2019,11,8,12,count)
            dvk.set_rating(count)
            dvk.set_views(count)
            dvk.write_dvk()
            count = count + 1
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        rmtree(self.test_dir.absolute())
        
    def test_reset_sorted(self):
        """
        Tests the reset_sorted function of the DvkHandler class.
        """
        dvk_handler = DvkHandler()
        dvk_handler.load_dvks([self.test_dir.absolute()])
        assert dvk_handler.get_size() == 8
        count = 0
        while count < len(dvk_handler.sorted):
            assert dvk_handler.sorted[count] == count
            count = count + 1
        dvk_handler.load_dvks()
        assert dvk_handler.sorted == []
        
    def test_get_dvk_direct(self):
        """
        Tests the get_dvk_direct function of the DvkHandler class.
        """
        dvk_handler = DvkHandler()
        dvk_handler.load_dvks([self.test_dir.absolute()])
        assert dvk_handler.get_dvk_direct().title == ""
        assert dvk_handler.get_dvk_direct(-1).title == ""
        assert dvk_handler.get_dvk_direct(8).title == ""
        titles = []
        for i in range(0, 8):
            dvk = dvk_handler.get_dvk_direct(i)
            assert not dvk.title in titles
            titles.append(dvk.title)
    
    def test_get_size(self):
        """
        Tests the get_size function of the DvkHandler class.
        """
        dvk_handler = DvkHandler()
        dvk_handler.load_dvks([self.test_dir.absolute()])
        assert dvk_handler.get_size() == 8
        dvk_handler.load_dvks(None)
        assert dvk_handler.get_size() == 0
        dvk_handler.load_dvks([Path(self.test_dir.joinpath("sub1").absolute()).absolute()])
        assert dvk_handler.get_size() == 2
        
    def test_get_directories(self):
        """
        Tests the get_directories function of the DvkHandler class.
        """
        dvk_handler = DvkHandler()
        paths = dvk_handler.get_directories([self.test_dir.absolute()])
        assert len(paths) == 4
        assert paths[0].name == "handlerTest"
        assert paths[1].name == "sub1"
        assert paths[2].name == "sub2"
        assert paths[3].name == "intSub"
        paths = dvk_handler.get_directories([Path(self.test_dir.joinpath("sub2").absolute()).absolute()])
        assert len(paths) == 2
        assert paths[0].name == "sub2"
        assert paths[1].name == "intSub"
        assert dvk_handler.get_directories() == []
        assert dvk_handler.get_directories(None) == []
        assert dvk_handler.get_directories("lskdfjo") == []
        paths = dvk_handler.get_directories([Path(self.test_dir.joinpath("sub1").absolute()).absolute(),
                                  Path(self.test_dir.joinpath("sub2").absolute()).absolute()])
        assert len(paths) == 3
        assert paths[0].name == "sub1"
        assert paths[1].name == "sub2"
        assert paths[2].name == "intSub"
        
        