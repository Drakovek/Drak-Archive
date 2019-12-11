from time import sleep
from io import BytesIO
from pathlib import Path
from bs4 import BeautifulSoup
from shutil import copyfileobj
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as CO
from selenium.webdriver.firefox.options import Options as FO
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import WebDriverException
from dvk_archive.processing.string_processing import get_extension


def print_driver_instructions():
    """
    Prints instructions for installing Selenium drivers.
    """
    print("This program uses Selenium to process JavaScript.")
    print("To run, you must install Selenium web drivers.")
    print("Download the drivers for your preferred browser:")
    print("")
    print("Firefox:")
    print("https://github.com/mozilla/geckodriver/releases")
    print("")
    print("Chrome/Chromium:")
    print("https://sites.google.com/a/chromium.org/chromedriver/downloads")
    print("")
    print("Copy Selenium driver(s) to your PATH directory.")
    print("(On Windows, find PATH with command \"echo %PATH%\" )")
    print("(On Mac/Linux, find PATH with command \"echo $PATH\" )")


class HeavyConnect:
    """
    Class for handling URL connections that require tokens or scripting.

    Attributes:
        driver (webdriver): Selenium webdriver for loading pages
    """

    def __init__(self, headless: bool = True):
        """
        Initializes the HeavyConnect class.
        """
        self.initialize_driver(headless)

    def initialize_driver(self, driver: str = "f", headless: bool = True):
        """
        Starts the selenium driver.

        Parameters:
            driver (str): Driver to use ("f" for firefox, "c" for chrome)
            headless (bool): Whether to run in headless mode
        """
        if driver == "f":
            try:
                # TRY FIREFOX DRIVER
                options = FO()
                options.set_headless(headless=headless)
                self.driver = webdriver.Firefox(options=options)
            except WebDriverException:
                self.initialize_driver("c", headless)
        else:
            try:
                # TRY CHROME DRIVER
                options = CO()
                options.set_headless(headless=headless)
                self.driver = webdriver.Chrome(options=options)
            except WebDriverException:
                self.driver = None
                print_driver_instructions()

    def get_page(
            self, url: str = None,
            wait: int = 0,
            element: str = None) -> BeautifulSoup:
        """
        Connects to a URL and returns a BeautifulSoup object.
        Capable of loading JavaScript, AJAX, etc.

        Parameters:
            url (str): URL to retrieve
            wait (int): Seconds to wait after initially loading the URL
            element (str): Element to wait for (XPATH) when loading URL

        Returns:
            BeautifulSoup: BeautifulSoup object of the url page
        """
        if url is None or url == "":
            return None
        try:
            self.driver.get(url)
            if wait > 0:
                sleep(wait)
            if element is not None and not element == "":
                WebDriverWait(self.driver, 10).until(
                     EC.presence_of_all_elements_located((By.XPATH, element)))
            bs = BeautifulSoup(self.driver.page_source, "lxml")
            return bs
        except (InvalidArgumentException, WebDriverException):
            return None
        return None

    def download(self, url: str = None, filename: str = None):
        """
        Downloads a file from a given url to a given file path.

        Parameters:
            url (str): URL from which to download
            filename (str): File path to save to
        """
        if (url is not None
                and not url == ""
                and filename is not None
                and not filename == ""):
            file = Path(filename)
            if file.exists():
                extension = get_extension(filename)
                base = filename[0:len(filename) - len(extension)]
                num = 1
                while file.exists():
                    file = Path(base + "(" + str(num) + ")" + extension)
                    num = num + 1
            # SAVE FILE
            try:
                byte_obj = BytesIO(self.driver.get(url))
                byte_obj.seek(0)
                with open(str(file.absolute()), "wb") as f:
                    copyfileobj(byte_obj, f)
            except (InvalidArgumentException, WebDriverException):
                print("Failed to download:" + url)

    def close_driver(self):
        """
        Closes the selenium driver, if possible.
        """
        if self.driver is not None:
            self.driver.close()
