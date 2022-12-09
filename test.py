from async_fetcher import AsyncFetcher
from awesome_parser import AwesomeParser

import asyncio
import pytest

START_URL = "https://ngs.ru"

BROKEN_URL = "https://twitter.com"

@pytest.mark.parametrize(
    argnames="url, expected_status",
    argvalues=[
        (START_URL, 200),
        (BROKEN_URL, 0),
    ],
    ids=["ngs", "twitter"]
)
def test_async_fethcher(url: str, expected_status: int):
    status, text, url, depth = asyncio.run(AsyncFetcher.get_texts_from_pages([(url,0)]))[0]
    assert status == expected_status


def test_parser():
    with open("test_page.html") as f:
        TEST_HTML = f.read()

    page_info = AwesomeParser.get_title_and_body_from_html_str(TEST_HTML)
    print(page_info)
    assert page_info.title == "It must be title!"
    assert page_info.body.strip() == "Hello, guys!"

