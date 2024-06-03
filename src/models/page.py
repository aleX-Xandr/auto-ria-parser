from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import  Optional
from urllib.parse import urlparse, parse_qs


class Pagination(BaseModel):
    cur_page:int=0
    max_page:int=0

    def __iter__(self):
        return iter([self.cur_page, self.max_page])


class BasePage(BaseModel):
    url: str
    text: Optional[str] = None
    query_data: dict = {}
    __soup: Optional[BeautifulSoup] = None
    
    @property
    def headers(self) -> dict:
        return {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            # 'cookie': 'Path=/; chk=1; __utma=79960839.414505191.1717407109.1717407109.1717407109.1; __utmc=79960839; __utmz=79960839.1717407109.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=79960839.2.10.1717407109; _ga=GA1.1.962960160.1717407111; _gcl_au=1.1.275174289.1717407111; Path=/; _fbp=fb.1.1717407113791.1742510685; test_new_features=442; advanced_search_test=42; promolink2=1; showNewFeatures=7; _504c2=http://10.42.19.107:3000; FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CP_oksAP_oksAEsACBRUA3EgAAAAAEPgAAggAAAOhQD2F2K2kKFkPCmQWYAQBCijYEAhQAAAAkCBIAAgAUgQAgFIIAgAIFAAAAAAAAAQEgCQAAQABAAAIACgAAAAAAIAAAAAAAQQAAAAAIAAAAAAAAEAAAAAAAQAAAAIAABEhCAAQQAEAAAAAAAQAAAAAAAAAAABAAA%22%2C%222~~dv.70.89.93.108.122.149.196.259.311.313.323.358.415.449.486.494.495.540.574.609.827.864.981.1029.1048.1051.1095.1097.1126.1205.1211.1276.1301.1365.1415.1423.1449.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.2072.2253.2299.2357.2373.2415.2506.2526.2568.2571.2575.2624.2677%22%2C%2225216E86-3C29-427B-B224-667894EFD1AF%22%5D%5D; __eoi=ID=473b0df805d5edb2:T=1717407221:RT=1717407221:S=AA-AfjZjnTYH0BcOD8oS4YEiLMix; _ga_KGL740D7XD=GS1.1.1717407110.1.1.1717407231.56.0.1762085934',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://auto.ria.com/',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }
    
    @property
    def payload(self) -> dict:
        return self.query_data
    
    @property
    def soup(self) -> BeautifulSoup:
        if self.__soup is None:
            self.__soup = BeautifulSoup(self.text, 'html.parser')
        return self.__soup


class CarPage(BasePage):
    pass


class CarsPage(BasePage):
    page: int = 0
    size: int = 100 # works for some endpoints eg /search, bigger size - less requests

    @property
    def payload(self) -> dict:
        return {
            **self.query_data,
            'page': self.page,
            'size': self.size
        }
    
    @classmethod
    def from_raw_url(cls, url: str) -> "CarsPage":

        url_object = urlparse(url)
        url = url.split("?")[0]
        query_data = parse_qs(url_object.query)
        query_data = {key: val[0] for key, val in query_data.items()}

        if url == "https://auto.ria.com/car/used/":
            url = "https://auto.ria.com/search/"
            query_data.update(type="bu", category_id=1)

        return cls(
            url = url,
            page = query_data.get("page", 0),
            query_data = query_data
        )
