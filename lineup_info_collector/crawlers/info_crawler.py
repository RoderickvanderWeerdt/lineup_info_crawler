import requests
from bs4 import BeautifulSoup
from unidecode import unidecode


from lineup_info_collector import constants


def _find_info_url(artist):
    source_code = requests.get(
        "https://www.allmusic.com/search/artists/" + artist, headers=constants.HEADERS
    )
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features="lxml")

    for div in soup.findAll("div", {"class": "artist"}):
        tag = """<a href="""
        url = str(div)[str(div).find(tag) + len(tag) + 1 :]
        url = url[: url.find("""\"""")]
        return url

def _compare_names(line_up_name, info_name):
    line_up_name = unidecode(line_up_name.lower())
    info_name = unidecode(info_name.lower()).replace("&amp;", "&") #allmusic replaces & with &amp; 
    return line_up_name == info_name

def _get_info(act_name, info_url, act_url, verbose):
    try:
        source_code = requests.get(info_url, headers=constants.HEADERS)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(f"ERROR: unable to get response from {info_url}")
        raise SystemExit(e)

    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features="lxml")

    name = ""
    activeDate = ""
    genres = []
    styles = []

    for div in soup.findAll("h1", {"id": "artistName"}):
        tag = """id="artistName">"""
        name = str(div)[str(div).find(tag) + len(tag) : -len("</h1>")]

    if _compare_names(act_name, name):
        for div in soup.findAll("div", {"class": "activeDates"}):
            activeDate = str(div)[
                str(div).find("<div>") + len("<div>") : -len("</div>\n</div>")
            ]
        for div in soup.findAll("div", {"class": "genre"}):
            for a in div.findAll("a"):
                genres.append(a.string)
        for div in soup.findAll("div", {"class": "styles"}):
            for a in div.findAll("a"):
                styles.append(a.string)
    else:
        print(f"{act_name} INFO: found information link did not match act name.")
    if verbose:
        print(
            f"{name:<40} | {activeDate:<13} | {';'.join(genres):<28} |{';'.join(styles)}"
        )
    return {
        "name": act_name,
        "activeDate": activeDate,
        "genres": ";".join(genres),
        "styles": ";".join(styles),
        "act_url": act_url,
        "info_url": info_url,
    }


def info_crawler(artists, verbose):
    all_info = []
    for artist in artists:
        info_url = _find_info_url(artist["name"])
        all_info.append(_get_info(artist["name"], info_url, artist["link"], verbose))
    return all_info
