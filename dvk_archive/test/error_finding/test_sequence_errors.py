#!/usr/bin/env python3

from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.error_finding.sequence_errors import get_sequence_errors
from dvk_archive.test.temp_dir import get_test_dir
from os.path import basename, join

def test_get_sequence_errors():
    """
    Tests the get_sequence_errors function.
    """
    # Test finding wrongly marked single Dvks
    test_dir = get_test_dir()
    single = Dvk()
    single.set_dvk_file(join(test_dir, "marked.dvk"))
    single.set_dvk_id("ID123")
    single.set_title("Marked")
    single.set_artist("artist")
    single.set_page_url("/url/")
    single.set_media_file("media.txt")
    single.set_first()
    single.set_last()
    single.write_dvk()
    single.set_dvk_file(join(test_dir, "unmarked.dvk"))
    single.set_title("Unmarked")
    single.set_prev_id(None)
    single.set_next_id(None)
    single.write_dvk()
    single.set_dvk_file(join(test_dir, "start.dvk"))
    single.set_title("Invalid Start")
    single.set_first()
    single.set_next_id("OTH123")
    single.write_dvk()
    single.set_dvk_file(join(test_dir, "end.dvk"))
    single.set_title("Invalid End")
    single.set_prev_id("OTH123")
    single.set_last()
    single.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    assert dvk_handler.get_size() == 4
    errors = get_sequence_errors(test_dir)
    assert len(errors) == 2
    assert len(errors[0]) == 1
    assert len(errors[1]) == 1
    assert basename(errors[0][0]) == "end.dvk"
    assert basename(errors[1][0]) == "start.dvk"
    # Test finding sequence that refrerences non-existant IDs
    test_dir = get_test_dir()
    pair = Dvk()
    pair.set_dvk_file(join(test_dir, "pair1_start.dvk"))
    pair.set_dvk_id("PRS01")
    pair.set_title("Pair 1 Start")
    pair.set_artist("artist")
    pair.set_page_url("url")
    pair.set_media_file("media.txt")
    pair.set_first()
    pair.set_next_id("PRE01")
    pair.write_dvk()
    pair.set_dvk_file(join(test_dir, "pair1_end.dvk"))
    pair.set_dvk_id("PRE01")
    pair.set_title("Pair 1 End")
    pair.set_prev_id("PRS01")
    pair.set_next_id("NONEXISTANT01")
    pair.write_dvk()
    pair.set_dvk_file(join(test_dir, "pair2_start.dvk"))
    pair.set_dvk_id("PRS02")
    pair.set_title("Pair 2 Start")
    pair.set_prev_id("NONEXISTANT02")
    pair.set_next_id("PRE02")
    pair.write_dvk()
    pair.set_dvk_file(join(test_dir, "pair2_end.dvk"))
    pair.set_dvk_id("PRE02")
    pair.set_title("Pair 2 End")
    pair.set_prev_id("PRS02")
    pair.set_last()
    pair.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    assert dvk_handler.get_size() == 4
    errors = get_sequence_errors(test_dir)
    assert len(errors) == 2
    assert len(errors[0]) == 2
    assert len(errors[1]) == 2
    assert basename(errors[0][0]) == "pair1_start.dvk"
    assert basename(errors[0][1]) == "pair1_end.dvk"
    assert basename(errors[1][0]) == "pair2_start.dvk"
    assert basename(errors[1][1]) == "pair2_end.dvk"
    # Test finding sequence with the same Dvk multiple times
    test_dir = get_test_dir()
    loop = Dvk()
    loop.set_dvk_file(join(test_dir, "loop1.dvk"))
    loop.set_dvk_id("LOOP01")
    loop.set_title("Loop 1")
    loop.set_artist("artist")
    loop.set_page_url("/url/")
    loop.set_media_file("media.txt")
    loop.set_prev_id("LOOP03")
    loop.set_next_id("LOOP02")
    loop.write_dvk()
    loop.set_dvk_file(join(test_dir, "loop2.dvk"))
    loop.set_dvk_id("LOOP02")
    loop.set_title("Loop 2")
    loop.set_prev_id("LOOP01")
    loop.set_next_id("LOOP03")
    loop.write_dvk()
    loop.set_dvk_file(join(test_dir, "loop3.dvk"))
    loop.set_dvk_id("LOOP03")
    loop.set_title("Loop 3")
    loop.set_prev_id("LOOP02")
    loop.set_next_id("LOOP01")
    loop.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    assert dvk_handler.get_size() == 3
    errors = get_sequence_errors(test_dir)
    assert len(errors) == 1
    assert len(errors[0]) == 3
    assert basename(errors[0][0]) == "loop1.dvk"
    assert basename(errors[0][1]) == "loop2.dvk"
    assert basename(errors[0][2]) == "loop3.dvk"
    # Test functional sequence with no errors
    test_dir = get_test_dir()
    seq = Dvk()
    seq.set_dvk_file(join(test_dir, "start.dvk"))
    seq.set_dvk_id("SEQ01")
    seq.set_title("Sequence Start")
    seq.set_artist("artist")
    seq.set_page_url("/url/")
    seq.set_media_file("media.txt")
    seq.set_first()
    seq.set_next_id("SEQ02")
    seq.write_dvk()
    seq.set_dvk_file(join(test_dir, "middle.dvk"))
    seq.set_dvk_id("SEQ02")
    seq.set_title("Sequence Middle")
    seq.set_prev_id("SEQ01")
    seq.set_next_id("SEQ03")
    seq.write_dvk()
    seq.set_dvk_file(join(test_dir, "end.dvk"))
    seq.set_dvk_id("SEQ03")
    seq.set_title("Sequence End")
    seq.set_prev_id("SEQ02")
    seq.set_last()
    seq.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    assert dvk_handler.get_size() == 3
    errors = get_sequence_errors(test_dir)
    assert len(errors) == 0
    # Test that Dvks link properly in both directions
    seq.set_prev_id(None)
    seq.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    assert dvk_handler.get_size() == 3
    errors = get_sequence_errors(test_dir)
    assert len(errors) == 1
    assert len(errors[0]) == 3
    assert basename(errors[0][0]) == "start.dvk"
    assert basename(errors[0][1]) == "middle.dvk"
    assert basename(errors[0][2]) == "end.dvk"
    seq.set_prev_id("SEQ02")
    seq.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    assert dvk_handler.get_size() == 3
    errors = get_sequence_errors(test_dir)
    assert len(errors) == 0
    seq.set_dvk_file(join(test_dir, "middle.dvk"))
    seq.set_title("Sequence Middle")
    seq.set_dvk_id("SEQ02")
    seq.set_prev_id("SEQ01")
    seq.set_next_id(None)
    seq.write_dvk()
    dvk_handler = DvkHandler(test_dir)
    assert dvk_handler.get_size() == 3
    errors = get_sequence_errors(test_dir)
    assert len(errors) == 1
    assert len(errors[0]) == 3
    assert basename(errors[0][0]) == "start.dvk"
    assert basename(errors[0][1]) == "middle.dvk"
    assert basename(errors[0][2]) == "end.dvk"
    # Thest getting Dvks using invalid parameters
    assert get_sequence_errors("/non/existant/dir/") == []
    assert get_sequence_errors(seq.get_dvk_file()) == []
    assert get_sequence_errors(None) == []

def all_tests():
    """
    Runs all tests for the sequence_errors.py module.
    """
    test_get_sequence_errors()
