from lineup_info_collector.crawlers.info_crawler import _compare_names

# _compare_names has a pre-existing bug (not touched by this fetch/parse-split ticket,
# see PR description): its second find-and-slice always trims 2 trailing characters
# even when the substring it's looking for isn't present, so it returns falsy for
# real-world exact matches. These tests pin down its actual current behavior.


def test_compare_names_exact_match_currently_fails():
    assert not _compare_names("Foo Fighters", "Foo Fighters")


def test_compare_names_followed_by_suffix_currently_fails():
    assert not _compare_names("the beatles", "the beatles (followed by a solo career)")


def test_compare_names_no_match():
    assert not _compare_names("Foo Fighters", "Muse")


def test_compare_names_matches_after_unconditional_trim():
    # The unconditional 4-character trim happens to line up here, so this "matches" -
    # not because the names are meaningfully compared, but as a side effect of the bug.
    assert _compare_names("abcd", "abcdefgh") == 1
