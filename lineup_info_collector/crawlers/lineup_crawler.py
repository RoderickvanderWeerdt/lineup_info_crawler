import requests
from bs4 import BeautifulSoup

from lineup_info_collector import constants


def _get_soup(url):
    try:
        response = requests.get(url, headers=constants.HEADERS)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(f"ERROR: failed to get response from website {url}")
        raise SystemExit(e)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def _dtrh_crawler(params):
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.findAll("a", {"class": "group"}):
        artists.append({"name": div.attrs["title"], "link": div.attrs["href"]})
    return artists


def _pinkpop_crawler_old(params: dict[str, str]) -> list[dict[str, str]]:
    """Crawls the Pinkpop website for artists.

    Args:
        params: A dictionary containing the URL of the festival.

    Returns:
        A list of dictionaries, where each dictionary represents an artist
        and contains the artist's name, a link to their page, and the day
        they are performing.

    Raises:
        ValueError: If no artist elements are found on the page.
    """
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.findAll("a", {"data-day": ["friday", "saturday", "sunday"]}):
        artist_name = div.text.strip()[div.text.strip().find("juni")+len("juni"):] #remove day from name
        artist_day = div.text.strip().split(' ')[0]
        artists.append({"name": artist_name, "link": div.attrs["href"], "day": artist_day})
    return artists

def _pinkpop_crawler(params):
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.findAll("a", {"data-day": ["friday", "saturday", "sunday"]}):
        artist_name = div.text.strip()[div.text.strip().find("juni")+len("juni"):] #remove day from name
        artist_day = div.text.strip().split(' ')[0]
        artists.append({"name": artist_name, "link": div.attrs["href"], "day": artist_day})
    return artists


def _ooto_crawler(params: dict[str, str]) -> list[dict[str, str]]:
    """Crawls the Out of the Ordinary website for artists.

    Args:
        params: A dictionary containing the URL of the festival.

    Returns:
        A list of dictionaries, where each dictionary represents an artist
        and contains the artist's name and a placeholder link.

    Raises:
        ValueError: If no artist elements are found on the page.
    """
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.findAll("a", {"data-day": ["friday", "saturday", "sunday"]}):
        artist_name = ' '.join(div.text.strip().split(' ')[:-3]) #remove day from name
        artist_day = div.text.strip().split(' ')[-3]
        artists.append({"name": artist_name, "link": div.attrs["href"], "day": artist_day})
    return artists

def _ooto_crawler(params):
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.find_all('h3'):
        artists.append({"name": div.text.strip(), "link": "~"})
    return artists

def _prettypissed_crawler(params):
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.findAll("a", {"class": "styles_page-preview-medium__link__Biqrh"}):
        artists.append({"name": div.text.strip(), "link": "https://www.melkweg.nl"+div.attrs["href"]})
    return artists

def _lowlands_crawler(params):
    soup = _get_soup(params["URL"])
    urls = []
    artists = []
    # first collect all the act pages
    for div in soup.findAll("a", {"class": "act-list-item__button"}):
        urls.append("https://lowlands.nl"+div.attrs["href"])

    # now get the act names from each url page
    for url in urls:
        soup = _get_soup(url)
        div = soup.find("h1", {"class": "detail-header__heading--large"})
        if div is None:
            print(f"Act url not working: {url}")
            continue
        name = div.text
        if name.startswith("black"):
            print(name)
        name = name.replace(",",";")
        if name.startswith("black"):
            print(name)
        artists.append({"name": name, "link": url})
    return artists

def _get_lowlands_styles(url):
    soup = _get_soup(url)
    div = soup.find("h2", {"class": "act-detail__subtitle"})
    if div is None:
        print(f"Act url not working: {url}")
        return ""
    return div.text.strip()

def _lowlands_crawler2(params):
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.findAll("a", {"class": "act-list-item__button"}):
        href = "https://www.lowlands.nl"+div.attrs["href"]
        artists.append({"name": div.text.strip(), "link": href, "backup_styles": _get_lowlands_styles(href)})
    return artists

def _str_dayfinder(txt, day):
    if txt.find(day) >= 0:
        return day
    else: return 0

def _str_weekend_dayfinder(txt):
    if _str_dayfinder(txt, "Friday"): return "Friday"
    elif _str_dayfinder(txt, "Saturday"): return "Saturday"
    elif _str_dayfinder(txt, "Sunday"): return "Sunday"

def _bks_crawler(params):
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.findAll("a", {"class": "act"}):
        artists.append({"name": div.figure.div.h3.text.strip(), "link": "https://www.bestkeptsecret.nl"+div.attrs["href"], "day": _str_weekend_dayfinder(div.text.strip()), "backup_styles": div.figure.div.span.text.strip()})
    return artists


def _str_weekend_dayfinder(txt):
    if _str_dayfinder(txt, "Friday"): return "Friday"
    elif _str_dayfinder(txt, "Saturday"): return "Saturday"
    elif _str_dayfinder(txt, "Sunday"): return "Sunday"

def _bks_crawler(params):
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.findAll("a", {"class": "act"}):
        artists.append({"name": div.figure.div.h3.text.strip(), "link": "https://www.bestkeptsecret.nl"+div.attrs["href"], "day": _str_weekend_dayfinder(div.text.strip()), "backup_styles": div.figure.div.span.text.strip()})
    return artists

def lineup_crawler(params):
    if params["FESTIVAL"] == "DTRH":
        return _dtrh_crawler(params)
    elif params["FESTIVAL"] == "lowlands":
        return _lowlands_crawler2(params)
    elif params["FESTIVAL"] == "pinkpop":
        return _pinkpop_crawler(params)
    elif params["FESTIVAL"] == "ooto":
        return _ooto_crawler(params)
    elif params["FESTIVAL"] == "prettypissed":
        return _prettypissed_crawler(params)
    elif festival_name == "BKS":
        return _bks_crawler(params)
    raise ValueError(
        f"Unknown festival {festival_name}. "
        "Currently accepted are: ['DTRH', 'lowlands', 'pinkpop', 'ooto', 'prettypissed']"
    )
