from lineup_info_collector.crawlers.festivals.dtrh import parse_dtrh


def test_parse_dtrh(load_fixture):
    soup = load_fixture("dtrh.html")
    assert parse_dtrh(soup) == [
        {"name": "Artist One", "link": "/artists/one"},
        {"name": "Artist Two", "link": "/artists/two"},
    ]
