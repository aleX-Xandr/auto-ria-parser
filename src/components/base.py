import aiohttp
import asyncio

from abc import ABC, abstractmethod
from typing import Any

from models.page import BasePage


class BaseParser(ABC):
    @staticmethod
    async def parse_content(page: BasePage) -> None:
        async with aiohttp.ClientSession(headers=page.headers) as session:
            async with session.get(page.url, params=page.payload) as response:
                page.text = await response.text()

    @abstractmethod
    def get_data(page: BasePage) -> Any:
        ...


class BaseWorker:
    processor: BaseParser

    def __init__(self, queue: asyncio.Queue) -> None:
        self.queue = queue
        print("init worker")

    async def parse(self) -> BasePage:
        page = await self.queue.get()
        await self.processor.parse_content(page)
        print("PARSED_LINK: ", page.url)
        self.queue.task_done()
        return page
    
    async def run(self):
        while True:
            await self.parse()