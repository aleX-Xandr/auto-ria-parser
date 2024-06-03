import logging

from abc import ABC, abstractmethod
from asyncio import Queue, create_task, gather, sleep

from components.parser import BaseDataParser, CarParser, CarsDataParser
from config import THREADAS_LIMIT, TARGET_URL
from loader import db
from models.page import BasePage, CarPage, CarsPage
from models.post import CarAdvertisement


class BaseWorker(ABC):
    processor: BaseDataParser

    def __init__(self, worker_queue: Queue) -> None:
        self.worker_queue = worker_queue

    async def parse(self, page: BasePage) -> BasePage:
        await self.processor.parse_content(page)
        logging.debug(f"PARSED_LINK: {page.url}")
        return page
    
    @abstractmethod
    async def callback(self, page: BasePage) -> None:
        ...

    async def run(self):
        while True:
            page = await self.worker_queue.get()
            page = await self.parse(page)
            for result in self.processor.get_data(page):
                await self.callback(result)
            self.worker_queue.task_done()

    def __del__(self) -> None:
        logging.debug(f"{self.__class__.__name__} WORKER STOPPED") 

class PostWorker(BaseWorker):
    processor: CarParser = CarParser

    async def callback(self, car_advertisement: CarAdvertisement) -> None:
        logging.debug(f"PARSED AD: {car_advertisement.url} : {car_advertisement.title}")
        async with db.get_session() as session:
            session.add(car_advertisement)
        await sleep(0)

class PageWorker(BaseWorker):
    processor: CarsDataParser = CarsDataParser

    def __init__(self, page_queue: Queue, posts_queue: Queue) -> None:
        self.posts_queue = posts_queue
        super().__init__(worker_queue=page_queue)

    async def callback(self, car_page: CarPage) -> None:
        # logging.debug(f"PUT AD TO QUEUE: {car_page}")
        await self.posts_queue.put(car_page)
        await sleep(0)


class MainWorker:
    def __init__(self) -> None:
        self.start_page = CarsPage.from_raw_url(url=TARGET_URL)
        self.posts_queue = Queue()
        self.pages_queue = Queue()

        pages_worker = PageWorker(self.pages_queue, self.posts_queue)
        posts_worker = PostWorker(self.posts_queue)

        self.workers = [
            create_task(
                posts_worker.run() if i % 2 == 0 else pages_worker.run()
            ) 
            for i in range(THREADAS_LIMIT)
        ]

    async def fill_queue(self):
        for page_num in CarsDataParser.get_page_range(self.start_page):
            next_page = CarsPage(
                url=self.start_page.url,
                page=page_num,
                query_data=self.start_page.query_data
            )
            # logging.debug(f"PUT PAGE TO QUEUE: {next_page}")
            await self.pages_queue.put(next_page)
            await sleep(0)

    async def run(self):
        await CarsDataParser.parse_content(self.start_page)
        await self.fill_queue()

        # Ожидание завершения всех задач
        await gather(
            self.posts_queue.join(), 
            self.pages_queue.join(), 
            return_exceptions=True
        ) 
        await self.close_workers()

    async def close_workers(self):
        for w in self.workers:
            w.cancel()
        await gather(*self.workers, return_exceptions=True)
    