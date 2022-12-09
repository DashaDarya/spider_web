from dataclasses import dataclass
from urllib.parse import urljoin
from bs4 import BeautifulSoup

@dataclass
class PageInfo:
    title: str
    body: str


class AwesomeParser:
    @staticmethod
    def get_title_and_body_from_html_str(text: str) -> PageInfo:
        if not text:
            return PageInfo("", "")

        soup = BeautifulSoup(text, 'html.parser')
        try:
            title = soup.find("title").get_text()
        except AttributeError:
            title = ""

        try:
            body = soup.find("body").get_text()
        except AttributeError:
            body = ""

        return PageInfo(title=title, body=body)

    @staticmethod
    def get_all_links_from_page(text: str, base_url: str):
        if not text:
            return []
        result_links = []
        soup = BeautifulSoup(text, 'html.parser')
        for url in soup.find_all('a'):
            r = urljoin(base_url, url.get('href'))
            result_links.append(r)
        return result_links