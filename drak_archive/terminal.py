from os import getcwd
from pathlib import Path
from argparse import ArgumentParser
from drak_archive.error.error_finding import identical_ids
from drak_archive.error.error_finding import missing_media
from drak_archive.error.error_finding import unlinked_media


def parse_terminal():
    """
    Reads command line argument from the user.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "directory",
        help="Directory in which to preform operations.",
        nargs="?",
        type=str,
        default=str(getcwd()))
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-i",
        "--same-ids",
        help="Checks for DVK files with identical IDs.",
        action="store_true")
    group.add_argument(
        "-m",
        "--missing-media",
        help="Checks for DVK files whose media files are missing.",
        action="store_true")
    group.add_argument(
        "-u",
        "--unlinked-media",
        help="Checks for media files with no corresponding DVK files.",
        action="store_true")
    args = parser.parse_args()
    dir = Path(args.directory)
    if args.same_ids:
        print_paths(identical_ids([dir.absolute()]), dir)
    elif args.missing_media:
        print_paths(missing_media([dir.absolute()]), dir)
    elif args.unlinked_media:
        print_paths(unlinked_media([dir.absolute()]), dir)


def print_paths(paths: list = None, base_path: Path = None):
    """
    Prints a list of pathlib paths.

    Parameters:
        paths (list): Paths to print
        base_path (Path): Base path used for truncating path strings
    """
    if paths is not None:
        for path in paths:
            print(truncate_path(path, base_path))


def truncate_path(path: Path = None, base_path: Path = None) -> str:
    """
    Returns a shortened version of a given path string.
    Removes the base path string from the path to be truncated.

    Parameters:
        path (Path): Path to truncate
        base_path (Path): Base path to omit from the main path

    Returns:
        str: Shortened path string for the given path
    """
    if path is None:
        return ""
    path_str = str(path.absolute())
    if base_path is None:
        return path_str
    base_str = str(base_path.absolute())
    if path_str.startswith(base_str):
        return "..." + path_str[len(base_str):]
    return path_str
