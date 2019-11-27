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
    if dvk_handler is not None:
        handler = dvk_handler
    else:
        handler = DvkHandler()
        handler.load_dvks(dvk_directories)
    handler.sort_dvks("a", True)
    # CREATE LIST OF IDS
    print("Searching for DVK files with identical IDs:")
    ids = []
    size = handler.get_size()
    for i in range(0, size):
        ids.append(handler.get_dvk_sorted(i).get_id())
    # FIND IDENTICAL IDS
    s_ids = []
    for i in tqdm(range(0, size)):
        if i not in s_ids:
            for k in range(i + 1, size):
                if ids[i] == ids[k]:
                    if i not in s_ids:
                        s_ids.append(i)
                    s_ids.append(k)
    # CREATE PATH LIST
    identicals = []
    for id in s_ids:
        identicals.append(handler.get_dvk_sorted(int(id)).get_file())
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
    # FIND ALL MEDIA FILES
    print("Searching for all media files.")
    missing = []
    for path in tqdm(handler.paths):
        for f in listdir(path.absolute()):
            file = path.joinpath(str(f))
            if not str(file.absolute()).endswith(".dvk") and not file.is_dir():
                missing.append(file)
    # REMOVES UNLINKED MEDIA
    print("Searching for all unlinked media.")
    d_size = handler.get_size()
    for d_num in tqdm(range(0, d_size)):
        # GETS MEDIA FILES FROM DVK
        dvk = handler.get_dvk_direct(d_num)
        d_files = [dvk.get_media_file()]
        if dvk.get_secondary_file() is not None:
            d_files.append(dvk.get_secondary_file())
        # REMOVES FROM THE MISSING FILES LIST
        m_num = 0
        while m_num < len(missing):
            i = 0
            while i < len(d_files):
                if d_files[i] == missing[m_num]:
                    del d_files[i]
                    del missing[m_num]
                    i = i - 1
                    m_num = m_num - 1
                i = i + 1
            m_num = m_num + 1
            if len(d_files) == 0 or len(missing) == 0:
                break
    return missing
