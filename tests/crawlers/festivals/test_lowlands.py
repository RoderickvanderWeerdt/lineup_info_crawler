from bs4 import BeautifulSoup

from lineup_info_collector.crawlers.festivals.lowlands import (
    parse_lowlands,
    parse_lowlands_categories,
    parse_lowlands_style,
)


def test_parse_lowlands(load_fixture):
    soup = load_fixture("lowlands.html")
    assert parse_lowlands(soup) == [
        {"name": "Foo Fighters", "link": "https://www.lowlands.nl/acts/foo-fighters"},
    ]


def test_parse_lowlands_style(load_fixture):
    soup = load_fixture("lowlands_act.html")
    assert parse_lowlands_style(soup) == "Alternative Rock"


def test_parse_lowlands_style_missing_subtitle():
    soup = BeautifulSoup("<html><body></body></html>", "html.parser")
    assert parse_lowlands_style(soup) == ""


def test_parse_lowlands_categories(load_fixture):
    soup = load_fixture("lowlands.html")
    assert parse_lowlands_categories(soup) == {
        "/acts/foo-fighters": {"category": "Muziek", "genres": "Electronic, Pop"},
    }


def test_parse_lowlands_categories_missing_script():
    soup = BeautifulSoup("<html><body></body></html>", "html.parser")
    assert parse_lowlands_categories(soup) == {}


def test_parse_lowlands_categories_unparseable_script():
    soup = BeautifulSoup(
        '<html><body><script id="__NUXT_DATA__">not json</script></body></html>', "html.parser"
    )
    assert parse_lowlands_categories(soup) == {}
