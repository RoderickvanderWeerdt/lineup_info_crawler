from lineup_info_collector import _apply_backup_styles_fallback


def test_apply_backup_styles_fallback_fills_empty_styles():
    all_info = [{"name": "Foo Fighters", "styles": "", "backup_styles": "Rock"}]
    assert _apply_backup_styles_fallback(all_info) == [
        {"name": "Foo Fighters", "styles": "Rock", "backup_styles": "Rock"},
    ]


def test_apply_backup_styles_fallback_leaves_existing_styles():
    all_info = [{"name": "Foo Fighters", "styles": "Rock", "backup_styles": "Alt Rock"}]
    assert _apply_backup_styles_fallback(all_info) == [
        {"name": "Foo Fighters", "styles": "Rock", "backup_styles": "Alt Rock"},
    ]


def test_apply_backup_styles_fallback_applies_to_every_artist():
    all_info = [
        {"name": "A", "styles": "", "backup_styles": "Rock"},
        {"name": "B", "styles": "", "backup_styles": "Pop"},
    ]
    result = _apply_backup_styles_fallback(all_info)
    assert [artist["styles"] for artist in result] == ["Rock", "Pop"]
