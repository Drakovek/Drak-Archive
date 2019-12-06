from bs4 import BeautifulSoup
from requests import exceptions
from requests import Session


def basic_connect(url: str = None) -> BeautifulSoup:
    """
    Connects to a URL and returns a BeautifulSoup object.
    Incapable of working with JavaScript.

    Parameters:
        url (str): URL to retrieve

    Returns:
        BeautifulSoup: BeautifulSoup object of the url page
    """
    if url is None or url == "":
        return None
    session = Session()
    headers = {
        "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept-Language":
        "en-US,en;q=0.5"}
    try:
        request = session.get(url, headers=headers)
        bs = BeautifulSoup(request.text, features="lxml")
        return bs
    except (exceptions.ConnectionError, exceptions.MissingSchema):
        return None
    return None
