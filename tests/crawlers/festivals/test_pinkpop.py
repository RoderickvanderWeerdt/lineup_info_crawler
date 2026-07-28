from lineup_info_collector.crawlers.festivals.pinkpop import parse_pinkpop


def test_parse_pinkpop(load_fixture):
    soup = load_fixture("pinkpop.html")
    assert parse_pinkpop(soup) == [
        {"name": " Metallica", "link": "/artists/metallica", "day": "Vrijdag"},
        {"name": " Muse", "link": "/artists/muse", "day": "Zaterdag"},
    ]
