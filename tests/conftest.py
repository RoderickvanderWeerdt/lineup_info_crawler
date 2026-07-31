from pathlib import Path

import pytest
from bs4 import BeautifulSoup

FIXTURES_DIR = Path(__file__).parent / "crawlers" / "fixtures"


@pytest.fixture
def load_fixture():
    def _load(name: str) -> BeautifulSoup:
        return BeautifulSoup((FIXTURES_DIR / name).read_text(), "html.parser")

    return _load
