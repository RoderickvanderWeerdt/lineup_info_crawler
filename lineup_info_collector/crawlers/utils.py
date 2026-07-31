from bs4 import BeautifulSoup


def extract_streaming_links(soup: BeautifulSoup) -> dict[str, str]:
    """Scans a parsed page for Spotify, Apple Music, and YouTube artist URLs.

    Checks every anchor tag's href. Returns the first match found for each
    platform. Values are empty strings when no link is found.

    Args:
        soup: A BeautifulSoup object representing the parsed page.

    Returns:
        A dict with keys ``spotify_url``, ``apple_music_url``, ``youtube_url``.
    """
    result: dict[str, str] = {
        "spotify_url": "",
        "apple_music_url": "",
        "youtube_url": "",
    }
    for a in soup.find_all("a", href=True):
        href: str | list = a.get("href", "")
        if isinstance(href, list):
            href = href[0]
        if not isinstance(href, str):
            continue

        if not result["spotify_url"] and "open.spotify.com/artist" in href:
            result["spotify_url"] = href
        elif not result["apple_music_url"] and "music.apple.com" in href:
            result["apple_music_url"] = href
        elif not result["youtube_url"] and any(
            pattern in href
            for pattern in ("youtube.com/channel", "youtube.com/@", "youtube.com/user")
        ):
            result["youtube_url"] = href

        if all(result.values()):
            break  # All three found; no need to keep scanning

    return result
