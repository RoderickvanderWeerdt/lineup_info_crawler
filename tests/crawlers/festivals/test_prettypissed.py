from lineup_info_collector.crawlers.festivals.prettypissed import parse_prettypissed


def test_parse_prettypissed(load_fixture):
    soup = load_fixture("prettypissed.html")
    assert parse_prettypissed(soup) == [
        {"name": "Artist One", "link": "https://www.melkweg.nl/nl/agenda/artist-one"},
    ]
