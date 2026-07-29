from lineup_info_collector.crawlers.lineup_crawler import _ensure_default_keys


def test_ensure_default_keys_fills_missing_keys():
    artists = [{"name": "Foo Fighters", "link": "https://example.com/foo-fighters"}]
    assert _ensure_default_keys(artists) == [
        {"name": "Foo Fighters", "link": "https://example.com/foo-fighters", "day": None, "backup_styles": ""},
    ]


def test_ensure_default_keys_leaves_existing_keys_untouched():
    artists = [
        {"name": "Gorillaz", "link": "https://example.com/gorillaz", "day": "Sunday", "backup_styles": "Rock"},
    ]
    assert _ensure_default_keys(artists) == [
        {"name": "Gorillaz", "link": "https://example.com/gorillaz", "day": "Sunday", "backup_styles": "Rock"},
    ]


def test_ensure_default_keys_fills_only_the_missing_one():
    artists = [{"name": "Metallica", "link": "https://example.com/metallica", "day": "Friday"}]
    assert _ensure_default_keys(artists) == [
        {"name": "Metallica", "link": "https://example.com/metallica", "day": "Friday", "backup_styles": ""},
    ]
