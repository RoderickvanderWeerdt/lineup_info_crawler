from lineup_info_collector.crawlers.festivals.bks import _str_dayfinder, _str_weekend_dayfinder, parse_bks


def test_parse_bks(load_fixture):
    soup = load_fixture("bks.html")
    assert parse_bks(soup) == [
        {
            "name": "Foo Fighters",
            "link": "https://www.bestkeptsecret.nl/bands/foo-fighters",
            "day": "Friday",
            "backup_styles": "Rock",
        },
    ]


def test_str_dayfinder_found():
    assert _str_dayfinder("Show on Friday", "Friday") == "Friday"


def test_str_dayfinder_not_found():
    assert _str_dayfinder("Show on Friday", "Sunday") == 0


def test_str_weekend_dayfinder_friday():
    assert _str_weekend_dayfinder("Show on Friday") == "Friday"


def test_str_weekend_dayfinder_saturday():
    assert _str_weekend_dayfinder("Show on Saturday") == "Saturday"


def test_str_weekend_dayfinder_sunday():
    assert _str_weekend_dayfinder("Show on Sunday") == "Sunday"


def test_str_weekend_dayfinder_none():
    assert _str_weekend_dayfinder("Show on Monday") is None
