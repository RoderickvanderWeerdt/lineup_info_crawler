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

def _pinkpop_crawler(params):
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

    artists = []
    for div in soup.findAll("a", {"class": "group"}):
        artists.append({"name": div.attrs["title"], "link": div.attrs["href"]})
    return artists


def lineup_crawler(params):
    if params["FESTIVAL"] == "DTRH":
        return _dtrh_crawler(params)
    elif params["FESTIVAL"] == "lowlands":
        return _lowlands_crawler(params)
    elif params["FESTIVAL"] == "pinkpop":
        return _pinkpop_crawler(params)
    elif params["FESTIVAL"] == "ooto":
        return _ooto_crawler(params)
    elif params["FESTIVAL"] == "prettypissed":
        return _prettypissed_crawler(params)
    else:
        exit(
            f"unknown festival {params['FESTIVAL']}. Currently accepted are: ['DTRH', 'lowlands', 'pinkpop', 'ooto']"
        )
