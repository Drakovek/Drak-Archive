from os import listdir
from tqdm import tqdm
from drak_archive.file.dvk_handler import DvkHandler


def identical_ids(
        dvk_directories: list = None,
        dvk_handler: DvkHandler = None) -> list:
    """
    Checks for Dvk objects with identical IDs.

    Parameters:
        dvk_directory (str): Directory from which to search for DVK files.
            Used if dvk_handler is None
        dvk_handler (list): DvkHandler with loaded DVK files.

    Returns:
        list: List of Paths for DVK files with identical IDs
    """
    located = []
    identicals = []
    if dvk_handler is not None:
        handler = dvk_handler
    else:
        handler = DvkHandler()
        handler.load_dvks(dvk_directories)
    handler.sort_dvks("a", True)
    size = handler.get_size()
    print("Searching for DVK files with identical IDs:")
    for i in tqdm(range(0, size)):
        first = True
        if i not in located:
            for k in range(i + 1, size):
                dvk_i = handler.get_dvk_sorted(i)
                dvk_k = handler.get_dvk_sorted(k)
                if dvk_i.get_id() == dvk_k.get_id():
                    if first:
                        located.append(i)
                        identicals.append(dvk_i.get_file())
                    first = False
                    located.append(k)
                    identicals.append(dvk_k.get_file())
    return identicals


def missing_media(
        dvk_directories: list = None,
        dvk_handler: DvkHandler = None) -> list:
    """
    Checks for Dvk objects which have missing media files.

    Parameters:
        dvk_directory (str): Directory from which to search for DVK files.
            Used if dvk_handler is None
        dvk_handler (list): DvkHandler with loaded DVK files.

    Returns:
        list: List of Paths for DVK files with missing linked media files
    """
    if dvk_handler is not None:
        handler = dvk_handler
    else:
        handler = DvkHandler()
        handler.load_dvks(dvk_directories)
    missing = []
    handler.sort_dvks("a", True)
    size = handler.get_size()
    print("Searching for DVK files without media files:")
    for i in tqdm(range(0, size)):
        file = handler.get_dvk_sorted(i).get_media_file()
        s_file = handler.get_dvk_sorted(i).get_secondary_file()
        if not file.exists() or (s_file is not None and not s_file.exists()):
            missing.append(handler.get_dvk_sorted(i).get_file())
    return missing


def unlinked_media(
        dvk_directories: list = None,
        dvk_handler: DvkHandler = None) -> list:
    """
    Checks for files without corresponding DVK files.

    Parameters:
        dvk_directory (str): Directory from which to search for DVK files.
            Used if dvk_handler is None
        dvk_handler (list): DvkHandler with loaded DVK files.

    Returns:
        list: List of Paths for files with no corresponding DVK file
    """
    if dvk_handler is not None:
        handler = dvk_handler
    else:
        handler = DvkHandler()
        handler.load_dvks(dvk_directories)
    missing = []
    print("Searching for media without corresponding DVK files:")
    for dir in tqdm(handler.dvk_directories):
        for f in listdir(dir.directory_path.absolute()):
            file = dir.directory_path.joinpath(str(f))
            if not str(file.absolute()).endswith(".dvk") and not file.is_dir():
                include = True
                size = dir.get_size()
                for i in range(0, size):
                    if (dir.get_dvk(i).get_media_file() == file
                            or dir.get_dvk(i).get_secondary_file() == file):
                        include = False
                        break
                if include:
                    missing.append(file)
    return missing
