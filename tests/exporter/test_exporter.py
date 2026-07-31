from lineup_info_collector.exporter.exporter import _check_backup_styles


def test_check_backup_styles_fills_empty_styles():
    artist = {"name": "Foo Fighters", "styles": "", "backup_styles": "Rock"}
    assert _check_backup_styles(artist)["styles"] == "Rock"


def test_check_backup_styles_fills_semicolon_styles():
    artist = {"name": "Foo Fighters", "styles": ";", "backup_styles": "Rock"}
    assert _check_backup_styles(artist)["styles"] == "Rock"


def test_check_backup_styles_leaves_existing_styles():
    artist = {"name": "Foo Fighters", "styles": "Rock", "backup_styles": "Alt Rock"}
    assert _check_backup_styles(artist)["styles"] == "Rock"


def test_check_backup_styles_missing_backup_key():
    artist = {"name": "Foo Fighters", "styles": ""}
    assert _check_backup_styles(artist)["styles"] == ""
