from pathlib import Path
from _functools import cmp_to_key
from drak_archive.file.dvk import Dvk
from drak_archive.processing.list_processing import list_to_string
from drak_archive.processing.string_compare import compare_strings
from drak_archive.processing.string_compare import compare_alphanum


class DvkDirectory:
    """
    Class for handling all the DVK files within a given directory.

    Parameters:
        directory_path (Path): Path of DVK directory
        group_artists (bool): Whether to group DVKs of the same artist together
        dvks (list): List of Dvk objects read from directory_path
    """

    def __init__(self):
        """
        Initializes the DvkDirectory class.
        """
        self.directory_path = Path()
        self.group_artists = False
        self.dvks = []

    def read_dvks(self, directory_str: str = None):
        """
        Reads all of the DVK files in a given directory.
        Add DVKs to dvk list.

        Parameters:
            directory_str (str): String path of the DVK directory
        """
        self.dvks = []
        if directory_str is not None and not directory_str == "":
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
        if self.dvks is None:
            return 0
        else:
            return len(self.dvks)

    def get_dvk(self, index_int: int = 0) -> Dvk:
        """
        Returns the Dvk object from the dvks list of the given index.
        If index is out of range, returns a default DVK.

        Returns:
            Dvk: Dvk object from the given index
        """
        if (index_int is None
                or index_int < 0
                or not index_int < self.get_size()):
            return Dvk()
        else:
            return self.dvks[index_int]

    def sort_dvks(
            self,
            sort_type: str = None,
            group_artists_bool: bool = False):
        """
        Sorts all currently loaded DVK objects in dvks list.

        Parameters:
            sort_type (str): Sort type
                ("t": Time, "r": Ratings, "v": Views, "a": Alpha-numeric)
            group_artists_bool (bool): Whether to group DVKs of the same artist
        """
        self.group_artists = group_artists_bool
        if sort_type is not None and self.get_size() > 0:
            if sort_type == "t":
                comparator = cmp_to_key(self.compare_time)
            elif sort_type == "r":
                comparator = cmp_to_key(self.compare_ratings)
            elif sort_type == "v":
                comparator = cmp_to_key(self.compare_views)
            else:
                comparator = cmp_to_key(self.compare_alpha)
            self.dvks = sorted(self.dvks, key=comparator)

    def compare_alpha(self, x: Dvk = None, y: Dvk = None) -> int:
        """
        Compares two DVK objects alpha-numerically by their titles.

        Parameters:
            x (Dvk): 1st Dvk object to compare
            y (Dvk): 2nd Dvk object to compare

        Returns:
            int: Which Dvk should come first.
                -1 for x, 1 for y, 0 for indeterminate
        """
        if x is None or y is None:
            return 0
        result = 0
        if self.group_artists:
            result = self.compare_artists(x, y)
        if result == 0:
            result = compare_alphanum(x.get_title(), y.get_title())
        if result == 0:
            return compare_strings(x.get_time(), y.get_time())
        return result

    def compare_time(self, x: Dvk = None, y: Dvk = None) -> int:
        """
        Compares two DVK objects by their publication time.

        Parameters:
            x (Dvk): 1st Dvk object to compare
            y (Dvk): 2nd Dvk object to compare

        Returns:
            int: Which Dvk should come first.
                -1 for x, 1 for y, 0 for indeterminate
        """
        if x is None or y is None:
            return 0
        result = 0
        if self.group_artists:
            result = self.compare_artists(x, y)
        if result == 0:
            result = compare_strings(x.get_time(), y.get_time())
        if result == 0:
            return compare_alphanum(x.get_title(), y.get_title())
        return result

    def compare_ratings(self, x: Dvk = None, y: Dvk = None) -> int:
        """
        Compares two DVK objects by their ratings.

        Parameters:
            x (Dvk): 1st Dvk object to compare
            y (Dvk): 2nd Dvk object to compare

        Returns:
            int: Which Dvk should come first.
                -1 for x, 1 for y, 0 for indeterminate
        """
        if x is None or y is None:
            return 0
        result = 0
        if self.group_artists:
            result = self.compare_artists(x, y)
        if result == 0:
            if x.get_rating() < y.get_rating():
                return -1
            elif x.get_rating() > y.get_rating():
                return 1
            return self.compare_alpha(x, y)
        return result

    def compare_views(self, x: Dvk = None, y: Dvk = None) -> int:
        """
        Compares two DVK objects by their view counts.

        Parameters:
            x (Dvk): 1st Dvk object to compare
            y (Dvk): 2nd Dvk object to compare

        Returns:
            int: Which Dvk should come first.
                -1 for x, 1 for y, 0 for indeterminate
        """
        if x is None or y is None:
            return 0
        result = 0
        if self.group_artists:
            result = self.compare_artists(x, y)
        if result == 0:
            if x.get_views() < y.get_views():
                return -1
            if x.get_views() > y.get_views():
                return 1
            return self.compare_alpha(x, y)
        return result

    def compare_artists(self, x: Dvk = None, y: Dvk = None) -> int:
        x_artists = list_to_string(x.get_artists())
        y_artists = list_to_string(y.get_artists())
        return compare_alphanum(x_artists, y_artists)
