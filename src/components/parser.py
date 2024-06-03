import re

from aiohttp import ClientSession 
from abc import ABC, abstractmethod
from typing import Any, Iterable

from models.post import CarAdvertisement
from models.page import BasePage, CarPage, CarsPage, Pagination


class BaseDataParser(ABC):
    @staticmethod
    async def parse_content(page: BasePage) -> None:
        async with ClientSession(headers=page.headers) as sess:
            async with sess.get(page.url, params=page.payload) as resp:
                page.text = await resp.text()

    @abstractmethod
    def get_data(page: BasePage) -> Any:
        ...


class CarsDataParser(BaseDataParser):
    @staticmethod
    def from_html(page: CarsPage) -> list[int, int] | None:
        span = page.soup.find("span", class_="page-item dhide text-c")
        if span is None:
            print("Pages not found error")
            return None
        
        page_nums = span.text.replace(" ", "")
        cur_page, max_page = page_nums.split("/") # eg "1 / 100"
        return Pagination(cur_page=cur_page, max_page=max_page)

    @staticmethod
    def from_js(page: CarsPage) -> list[int, int] | None:
        pattern = r'window\.ria\.server\.resultsCount\s*=\s*Number\((\d+)\);'
        script_tags = page.soup.find_all('script')
        total = 0

        for script in script_tags:
            script_text = script.string
            if script_text:
                match = re.search(
                    pattern, 
                    script_text
                )
                if match:
                    total = int(match.group(1))
                    break
        else:
            print("Pages not found error")
            return None
        return Pagination(cur_page=page.page+1, max_page=int(total / page.size))

    @classmethod
    def get_page_range(cls, page: CarsPage):
        pagination_data = cls.from_js(page)
        if pagination_data is None:
            pagination_data = cls.from_html(page)
        if pagination_data is None:
            pagination_data = Pagination()
        return range(*pagination_data)

    @staticmethod
    def get_data(page: CarsPage) -> Iterable[CarPage]:
        for car_post in page.soup.select("div.content-bar > a.m-link-ticket"):
            yield CarPage(url=car_post["href"]) 
        

class CarParser(BaseDataParser):
    @staticmethod
    def get_data(page: CarPage) -> Iterable[CarAdvertisement]:
        yield CarAdvertisement.from_page(page)
    
