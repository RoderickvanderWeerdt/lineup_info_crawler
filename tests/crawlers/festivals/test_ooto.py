from lineup_info_collector.crawlers.festivals.ooto import parse_ooto


def test_parse_ooto(load_fixture):
    soup = load_fixture("ooto.html")
    assert parse_ooto(soup) == [
        {"name": "Artist One", "link": "~"},
        {"name": "Artist Two", "link": "~"},
    ]
