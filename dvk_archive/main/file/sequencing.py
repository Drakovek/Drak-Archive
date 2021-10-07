#!/usr/bin/env python3

from _functools import cmp_to_key
from argparse import ArgumentParser
from dvk_archive.main.file.dvk_handler import Dvk
from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.file.dvk_handler import get_directories
from dvk_archive.main.processing.list_processing import clean_list
from dvk_archive.main.processing.string_compare import compare_alphanum
from dvk_archive.main.processing.string_processing import pad_num
from os import getcwd, pardir
from os.path import abspath, basename, exists, isdir, join
from typing import List

def set_sequence_from_indexes(dvk_handler:DvkHandler=None,
                indexes:List[int]=[],
                seq_title:str=None):
    """
    Sets a group of Dvks as a sequence from DvkHandler indexes.

    :param dvk_handler: DvkHandler used to source Dvks, defaults to None
    :type dvk_handler: DvkHandler, optional
    :param indexes: Indexes of the Dvks to put in sequence, defaults to None
    :type indexes: list[int], optional
    :param seq_title: Sequence title for Dvk if desired, defaults to None
    :type seq_title: str, optional
    """
    if dvk_handler is not None and indexes is not None:
        # Get list of Dvks
        dvks = []
        for index in indexes:
            dvks.append(dvk_handler.get_dvk(index))
        # Set the sequence
        dvks = set_sequence(dvks, seq_title)
        # Set dvks in dvk_handler to thier new values
        for i in range(0, len(dvks)):
            dvk_handler.set_dvk(dvks[i], indexes[i])

def set_sequence(dvks:List[Dvk], seq_title:str=None) -> List[Dvk]:
    """
    Sets a group of Dvks as a sequence.

    :param dvks: List of Dvks to turn into a sequence, defaults to None
    :type dvks: list[Dvk] optional
    :param seq_title: Sequence title for Dvk if desired, defaults to None
    :type seq_title: str, optional
    :return: List of Dvks wit sequence data added
    :rtype: List[Dvk]
    """
    if dvks is None:
        return []
    sequenced = []
    sequenced.extend(dvks)
    total = len(sequenced)
    for i in range(0, total):
        # Get Dvk to edit from index
        edit_dvk = sequenced[i]
        # Set the previous ID
        if i == 0:
            # Set to first if first in the sequence
            edit_dvk.set_first()
        else:
            prev_dvk = sequenced[i-1]
            edit_dvk.set_prev_id(prev_dvk.get_dvk_id())
        # Set the next ID
        if i == len(sequenced) - 1:
            # Set to last if last in the sequence
            edit_dvk.set_last()
        else:
            next_dvk = sequenced[i+1]
            edit_dvk.set_next_id(next_dvk.get_dvk_id())
        # Set the sequence title
        if len(sequenced) > 1:
            edit_dvk.set_sequence_title(seq_title)
        else:
            edit_dvk.set_sequence_title()
        # Set the sequence number and total
        edit_dvk.set_sequence_total(total)
        edit_dvk.set_sequence_number(0)
        if total > 1:
            edit_dvk.set_sequence_number(i + 1)
        # Write Dvk and update the DvkHandler
        edit_dvk.write_dvk()
        sequenced[i] = edit_dvk
    return sequenced

def get_sequence(dvk_handler:DvkHandler=None, index:int=None) -> List[int]:
    """
    Gets a group of Dvks in a sequence from a given starting index.

    :param dvk_handler: DvkHandler to search through for Dvks, defaults to None
    :type dvk_handler: DvkHandler, optional
    :param index: Index of a Dvk in she sequence, defaults to None
    :type index: int, optional
    :return: List of indexes for the Dvks in the sequence
    :rtype: list[int]
    """
    try:
        # Get all Dvks from after the given index
        next_ids = []
        if index > -1:
            dvk = dvk_handler.get_dvk(index)
        while not dvk.is_last() and dvk.get_next_id() is not None:
            # Get next Dvk
            next_id = dvk.get_next_id()
            cur_index = dvk_handler.get_dvk_by_id(next_id)
            if cur_index == -1 or cur_index in next_ids:
                # Stop if Dvk doesn't exist or is already in sequence
                break
            next_ids.append(cur_index)
            dvk = dvk_handler.get_dvk(cur_index)
        # Get all Dvks from before the given index
        ids = []
        dvk = dvk_handler.get_dvk(index)
        while not dvk.is_first() and dvk.get_prev_id() is not None:
            # Get prev Dvk
            prev_id = dvk.get_prev_id()
            cur_index = dvk_handler.get_dvk_by_id(prev_id)
            if cur_index == -1 or cur_index in ids:
                # Stop if Dvk doesn't exist or is already in sequence
                break
            ids.append(cur_index)
            dvk = dvk_handler.get_dvk(cur_index)
        ids.reverse()
        # Combine lists of indexes
        ids.append(index)
        ids.extend(next_ids)
        return ids
    except:
        return []

def get_default_sequence_order(directory:str=None) -> List[Dvk]:
    """
    Returns a list of Dvks in the order they would be expected to be in a sequence.

    :param directory: Directory in which to look for Dvks, defaults to None
    :type directory: str, optional
    :return: List of Dvks in the default sequence order
    :rtype: list[Dvk]
    """
    # Get directories, then sort them
    directories = get_directories(directory)
    comparator = cmp_to_key(compare_alphanum)
    directories = sorted(directories, key=comparator)    
    # Get dvks in each directory and add to the list of dvks
    dvks = []
    for directory in directories:
        dvk_handler = DvkHandler(directory)
        dvk_handler.sort_dvks("a")
        for i in range(0, dvk_handler.get_size()):
            dvks.append(dvk_handler.get_dvk(i))
    # Check that there are no duplicates
    paths = []
    for dvk in dvks:
        paths.append(dvk.get_dvk_file())
    length = len(paths)
    paths = clean_list(paths)
    if not length == len(paths):
        print("Too many internal directories.")
        return []
    # Return list of sorted Dvks
    return dvks

def user_create_sequence(directory:str=None):
    """
    Allows the user to set a sequence as well as its sequence and section titles.

    :param directory: Directory in which to create sequence, defaults to None
    :type directory: str, optional
    """
    # Gets the default sequence order
    print("Getting DVKs...")
    dvks = get_default_sequence_order(directory)
    if dvks == []:
        print("Files are not arranged properly!")
    else:
        # Get folders of the different sections
        folders = []
        for dvk in dvks:
            print(dvk.get_title())
            parent = abspath(join(dvk.get_dvk_file(), pardir))
            if not parent in folders:
                folders.append(parent)
        # Get sequence title
        write_sequence = True
        print("")
        seq_title = str(input("Sequence Title (q to cancel):"))
        if seq_title == "q":
            write_sequence = False
        # Get section titles
        section_titles = []
        if write_sequence and len(folders) > 1:
            for i in range(0, len(folders)):
                show = "Section Title for: "\
                            +basename(folders[i])\
                            +" (q to cancel):"
                sec_title = str(input(show))
                section_titles.append(sec_title)
                if sec_title == "q":
                    write_sequence = False
                    break
        # Write sequence
        if write_sequence:
            dvks = set_sequence(dvks, seq_title)
            # Set sections if applicable
            if len(folders) > 1:
                for i in range(0, len(dvks)):
                    parent = abspath(join(dvks[i].get_dvk_file(), pardir))
                    while not parent == folders[0]:
                        del folders[0]
                        del section_titles[0]
                    dvks[i].set_section_title(section_titles[0])
                    dvks[i].write_dvk()
            print("Finished writing sequence!")
        else:
            print("Sequence writing canceled.")

def main():
    """
    Sets up commands for adding sequence data to DVK files.
    """
    parser = ArgumentParser()
    parser.add_argument(
            "directory",
            help="Directory in which to search for DVKs with missing linked media.",
            nargs="?",
            type=str,
            default=str(getcwd()))
    args = parser.parse_args()
    full_directory = abspath(args.directory)
    # Check if directory exists
    if (full_directory is not None
                and exists(full_directory)
                and isdir(full_directory)):
        user_create_sequence(full_directory)
    else:
        print("Invalid directory")

if __name__ == "__main__":
    main()

