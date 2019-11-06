from pathlib import Path
from _functools import cmp_to_key
from file.Dvk import Dvk
from processing.StringCompare import compare_alphanum

class DvkDirectory:
    """
    Class for handling all the DVK files within a given directory.
    
    Parameters:
        directory_path (Path): Path of the directory from which to read DVK files
        dvks (list): List of Dvk objects read from directory_path
    """
    
    def __init__(self):
        """
        Initializes the DvkDirectory class.
        """
        self.directory_path = Path()
        self.dvks = []
        
    def read_dvks(self, directory_str:str=None):
        """
        Reads all of the DVK files in a given directory, adding them to the dvks list.
        
        Parameters:
            directory_str (str): String path of the directory from which to search for DVK files
        """
        self.dvks = []
        if not directory_str == None and not directory_str == "":
            self.directory_path = Path(directory_str)
            dvk_files = self.directory_path.glob("*.dvk")
            for dvk_file in dvk_files:
                dvk = Dvk()
                dvk.set_file(dvk_file.absolute())
                dvk.read_dvk()
                self.dvks.append(dvk)
                
    def get_size(self) -> int:
        """
        Returns the size of the dvks list.
        
        Returns:
            int: Size of the dvks list.
        """
        if self.dvks == None:
            return 0
        else:
            return len(self.dvks)
        
    def get_dvk(self, index_int:int=0) -> Dvk:
        """
        Returns the Dvk object from the dvks list of the given index.
        If index is out of range, returns a default DVK.
        
        Returns:
            Dvk: Dvk object from the given index
        """
        if index_int == None or index_int < 0 or not index_int < self.get_size():
            return Dvk()
        else:
            return self.dvks[index_int]
    
    def sort_dvks(self):
        """
        Sorts all currently loaded DVK objects in dvks list.
        """
        if self.get_size() > 0:
            self.dvks = sorted(self.dvks, key=cmp_to_key(self.compare_dvks_alpha))

    def compare_dvks_alpha(self, x:Dvk=None, y:Dvk=None) -> str:
        """
        Compares two DVK objects alpha-numerically by their titles.
        
        Parameters:
            x (Dvk): 1st Dvk object to compare
            y (Dvk): 2nd Dvk object to compare
        
        Returns:
            int: Which Dvk should come first. -1 for x, 1 for y, 0 for indeterminate
        """
        if x == None or y == None:
            return 0
        return compare_alphanum(x.get_title(), y.get_title())
        
        