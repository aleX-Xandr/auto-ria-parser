from pydantic import BaseModel
from typing import  Optional
from urllib.parse import urlparse, parse_qs


class BasePage(BaseModel):
    url: str
    text: Optional[str] = None
    headers: dict = {
        'authority': 'auto.ria.com',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'referer': 'https://auto.ria.com/',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
                      'AppleWebKit/537.36 (KHTML, like Gecko) '\
                      'Chrome/118.0.0.0 Safari/537.36',
    }
    query_data: dict = {}

    @property
    def payload(self) -> dict:
        return self.query_data


class CarPost(BasePage):
    pass # TODO


class Page(BasePage):
    page: int = 0
    page_size: int = 100 # works for some endpoints eg /search, bigger size - less requests

    @property
    def payload(self) -> dict:
        return {
            **self.query_data,
            'page': self.page,
            'size': self.page_size
        }
    
    @classmethod
    def from_raw_url(cls, url: str) -> "Page":
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params = {key: val[0] for key, val in query_params.items()}
        page = query_params.get("page", 0)
        return cls(
            url = parsed_url.geturl(),
            page = page,
            query_data = query_params
        )
