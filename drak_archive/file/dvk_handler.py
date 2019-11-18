from os import walk
from pathlib import Path
from drak_archive.file.dvk import Dvk
from drak_archive.file.dvk_directory import DvkDirectory
from drak_archive.processing.list_processing import clean_list


class DvkHandler:
    """
    Handles Dvk objects for given directories and their sub-directories.

    Attributes:
        dvk_directories (list): Loaded DvkDirectories objects
        sorted (list): List of direct indexes to Dvks in a sorted order
    """

    def __init__(self):
        """
        Initializes DvkHandler attributes.
        """
        self.dvk_directories = []
        self.sorted = []

    def load_dvks(self, directory_strs: list = None):
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

    def get_dvk_sorted(self, index_int: int = -1) -> Dvk:
        """
        Returns the Dvk object for a given index in the sorted index list.

        Parameters:
            index_int (int): Sorted index

        Returns:
            Dvk: Dvk object for the given index
        """
        if index_int > -1 and index_int < self.get_size():
            return self.get_dvk_direct(self.sorted[index_int])
        return Dvk()

    def get_dvk_direct(self, index_int: int = -1) -> Dvk:
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
                size = self.dvk_directories[dir_index].get_size()
                if mod_index > -1 and mod_index < size:
                    return self.dvk_directories[dir_index].get_dvk(mod_index)
                else:
                    offset = offset + size
                dir_index = dir_index + 1
        return Dvk()

    def get_directories(self, directory_strs: list = None) -> list:
        """
        Returns a list of directories and sub-directories in a given file path.

        Parameters:
            directory_strs (list): Directories to search within

        Returns:
            list: Internal directories in the form of pathlib Path objects
        """
        if directory_strs is None:
            return []
        paths = []
        for d in directory_strs:
            if d is not None and not d == "":
                directory_path = Path(d)
                for p in walk(directory_path.absolute()):
                    paths.append(Path(p[0]))
        return sorted(clean_list(paths))

    def sort_dvks(
            self,
            sort_type: str = None,
            group_artists_bool: bool = False):
        """
        Sorts the indexes in sorted list based on loaded Dvk objects.

        Parameters:
            sort_type (str): Sort type
                ("t": Time, "r": Ratings, "v": Views, "a": Alpha-numeric)
            group_artists_bool (bool): Whether to group DVKs of the same artist
        """
        if self.get_size() > 0:
            # SORT INDIVIDUAL DIRECTORIES
            for dvk_directory in self.dvk_directories:
                dvk_directory.sort_dvks(sort_type, group_artists_bool)
            # SPLIT SORTED
            separated = []
            dir_index = 0
            index_int = 0
            while dir_index < len(self.dvk_directories):
                separated.append([])
                s = self.dvk_directories[dir_index].get_size() + index_int
                while index_int < s:
                    separated[dir_index].append(index_int)
                    index_int = index_int + 1
                dir_index = dir_index + 1
            # MERGE
            dd = self.dvk_directories[0]
            dd.group_artists = group_artists_bool
            while len(separated) > 1:
                merged = []
                while len(separated[0]) > 0 and len(separated[1]) > 0:
                    # COMPARE DVKS
                    dvk1 = self.get_dvk_direct(separated[0][0])
                    dvk2 = self.get_dvk_direct(separated[1][0])
                    if sort_type == "t":
                        result = dd.compare_time(dvk1, dvk2)
                    elif sort_type == "r":
                        result = dd.compare_ratings(dvk1, dvk2)
                    elif sort_type == "v":
                        result = dd.compare_views(dvk1, dvk2)
                    else:
                        result = dd.compare_alpha(dvk1, dvk2)
                    # ADD TO MERGE
                    if result > 0:
                        merged.append(separated[1][0])
                        del separated[1][0]
                    else:
                        merged.append(separated[0][0])
                        del separated[0][0]
                merged.extend(separated[0])
                del separated[0]
                merged.extend(separated[0])
                del separated[0]
                separated.append(merged)
            self.sorted = separated[0]
        else:
            self.reset_sorted()
