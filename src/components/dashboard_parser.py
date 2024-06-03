import asyncio

from bs4 import BeautifulSoup
from typing import Iterable

from components.base import BaseParser, BaseWorker
from models.page import CarPost, Page


class PageParser(BaseParser):
    @staticmethod
    def get_pages_range(page: Page) -> Iterable[int]:
        soup = BeautifulSoup(page.text, 'html.parser')
        span = soup.find('span', class_='page-item dhide text-c')
        page_nums = span.text.replace(" ", "")
        cur_page, max_page = page_nums.split("/") # eg "1 / 100"
        return range(int(cur_page), int(max_page))

    @staticmethod
    def get_data(page: Page) -> Iterable[CarPost]:
        soup = BeautifulSoup(page.text, 'html.parser')
        for car in soup.select('div.content-bar > a.m-link-ticket'):
            yield CarPost(url=car["href"]) 
            

class PageWorker(BaseWorker):
    processor: PageParser = PageParser
    def __init__(self, queue: asyncio.Queue, posts_queue: asyncio.Queue) -> None:
        self.queue = queue
        self.posts_queue = posts_queue

    async def run(self) -> None:
        while True:
            page = await self.parse()
            for car_post in PageParser.get_data(page):
                await self.posts_queue.put(car_post)

    
        