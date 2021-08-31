#!/usr/bin/env python3

from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.file.sequencing import get_sequence
from dvk_archive.main.processing.list_processing import clean_list
from os.path import exists, isdir
from tqdm import tqdm
from typing import List

def get_sequence_errors(directory:str=None) -> List[List[str]]:
    """
    Gets a list of DVK files with sequence errors in a given directory.

    :param directory: Directory in which to search for errors, defaults to None
    :type directory: str, optional
    :return: List of DVK paths grouped by sequence with sequence errors
    :rtype: list[list[str]]
    """
    # Return empty list if directory is invalid
    if directory is None or not exists(directory) or not isdir(directory):
        return []
    # Read Dvks for the given directory
    dvk_handler = DvkHandler(directory)
    dvk_handler.sort_dvks("a")
    # Run through all the dvks in the DvkHandler
    error_indexes = []
    checked_indexes = []
    size = dvk_handler.get_size()
    for index in tqdm(range(0, size)):
        # Only check Dvk if not alreadiy in checked list.
        if not index in checked_indexes:
            # Get sequence, then add to checked indexes
            seq = get_sequence(dvk_handler, index)
            checked_indexes.extend(seq)
            # Check if sequence has an invailid start or end
            if len(seq) > 0:
                base_dvk = dvk_handler.get_dvk(seq[0])
            if (len(seq) > 1 and
                        (not base_dvk.is_first()
                        or not dvk_handler.get_dvk(seq[len(seq)-1]).is_last())):
                # If sequence starts or ends without appropriate bookends
                error_indexes.append(seq)
            elif (len(seq) == 1 and
                        ((not base_dvk.is_first()
                        and base_dvk.get_prev_id() is not None)
                        or (not base_dvk.is_last()
                        and base_dvk.get_next_id() is not None))):
                # If single isn't unmarked or marked as single
                error_indexes.append(seq)
            else:
                # Test if all sequence ids are set correctly
                for seq_num in range(0, len(seq)):
                    base_dvk = dvk_handler.get_dvk(seq[seq_num])
                    # Test that previous ID is correct
                    if seq_num > 0:
                        prev_dvk = dvk_handler.get_dvk(seq[seq_num-1])
                        if not base_dvk.get_prev_id() == prev_dvk.get_dvk_id():
                            error_indexes.append(seq)
                            break
                    # Test that next ID is correct
                    if seq_num < len(seq)-1:
                        next_dvk = dvk_handler.get_dvk(seq[seq_num+1])
                        if not base_dvk.get_next_id() == next_dvk.get_dvk_id():
                            error_indexes.append(seq)
                            break
    # Get paths for the Dvks with sequence errors
    error_paths = []
    for seq in error_indexes:
        path_group = []
        for index in seq:
            path_group.append(dvk_handler.get_dvk(index).get_dvk_file())
        error_paths.append(clean_list(path_group))
    return error_paths
