from os import walk
from pathlib import Path
from file.Dvk import Dvk
from file.DvkDirectory import DvkDirectory
from processing.ListProcessing import clean_list
class DvkHandler:
    """
    Handles Dvk objects for given directories and their sub-directories.
    
    Attributes:
        dvk_directories (list): DvkDirectories objects from which to Dvk objects are loaded
        sorted (list): List of direct indexes to Dvks in a sorted order
    """
    
    def __init__(self):
        """
        Initializes DvkHandler attributes.
        """
        self.dvk_directories = []
        self.sorted = []
    
    def load_dvks(self, directory_strs:list=None):
        """
        Loads DVK files from a given directory and sub-directories.
        
        Parameters:
            directory_strs (list): Directories from which to load DVK files
        """
        self.dvk_directories = []
        paths = self.get_directories(directory_strs)
        for path in paths:
            dvk_directory = DvkDirectory()
            dvk_directory.read_dvks(path.absolute())
            self.dvk_directories.append(dvk_directory)
        self.reset_sorted()
        
    def reset_sorted(self):
        """
        Resets the sorted list to the default order.
        """
        self.sorted = []
        size = 0
        for dvk_directory in self.dvk_directories:
            size = size + dvk_directory.get_size()
        for i in range(0, size):
            self.sorted.append(i)
            
    def get_size(self) -> int:
        """
        Returns the number of DVK files loaded / size of sorted list.
        
        Returns:
            int: Number of DVK files loaded
        """
        return len(self.sorted)
        
    def get_dvk_direct(self, index_int:int=-1) -> Dvk:
        """
        Returns the Dvk object for a given direct index.
        
        Parameters:
            index_int (int): Direct index
            
        Returns:
            Dvk: Dvk object for the given index
        """
        if index_int > -1 and index_int < self.get_size():
            offset = 0
            dir_index = 0
            mod_index = 0
            while dir_index < len(self.dvk_directories):
                mod_index = index_int - offset
                if mod_index > -1 and mod_index < self.dvk_directories[dir_index].get_size():
                    return self.dvk_directories[dir_index].get_dvk(mod_index)
                else:
                    offset = offset + self.dvk_directories[dir_index].get_size()
                dir_index = dir_index + 1
        return Dvk()
      
    def get_directories(self, directory_strs:list=None) -> list:
        """
        Returns a list of directories and sub-directories in a given file path.
        
        Parameters:
            directory_strs (list): Directories from which to search for further directories
            
        Returns:
            list: Internal directories in the form of pathlib Path objects
        """
        if directory_strs == None:
            return []
        paths = []
        for d in directory_strs:
            if not d == None and not d == "":
                directory_path = Path(d)
                for p in walk(directory_path.absolute()):
                    paths.append(Path(p[0]))
        return sorted(clean_list(paths))
    
    