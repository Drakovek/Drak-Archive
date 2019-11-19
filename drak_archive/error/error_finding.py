from drak_archive.file.dvk_handler import DvkHandler


def identical_ids(
        dvk_directory: str = None,
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
        handler.load_dvks([dvk_directory])
    handler.sort_dvks("a", True)
    size = handler.get_size()
    for i in range(0, size):
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
