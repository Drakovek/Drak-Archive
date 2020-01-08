from traceback import print_exc
from dvk_archive.tests.error.test_error import test_error
from dvk_archive.tests.file.test_file import test_file
from dvk_archive.tests.processing.test_processing import test_processing
from dvk_archive.tests.reformat.test_reformat import test_reformat
from dvk_archive.tests.web.test_web import test_web


def test_all():
    """
    Runs all test cases.
    """
    try:
        test_error()
        test_file()
        test_processing()
        test_reformat()
        test_web()
        print("\033[32mAll dvk_archive tests passed.\033[0m")
    except AssertionError:
        print("\033[31mCheck failed:\033[0m")
        print_exc()


def main():
    test_all()


if __name__ == "__main__":
    main()
