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
    else:
        exit(
            f"unknown festival {params['FESTIVAL']}. Currently accepted are: ['DTRH', 'lowlands']"
        )
