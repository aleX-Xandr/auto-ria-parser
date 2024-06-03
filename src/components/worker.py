import asyncio

from config import THREADAS_LIMIT, TARGET_URL
from models.page import Page
from .car_parser import PostWorker
from .dashboard_parser import PageParser, PageWorker


class Worker:
    def __init__(self):
        self.posts_queue = asyncio.Queue()
        self.pages_queue = asyncio.Queue()

    async def run(self) -> None:
        # Запуск воркеров
        pages_worker = PageWorker(self.pages_queue, self.posts_queue)
        posts_worker = PostWorker(self.posts_queue)
        workers = [
            asyncio.create_task(
                pages_worker.run() if i % 2 == 0 else posts_worker.run()
            ) 
            for i in range(THREADAS_LIMIT)
        ]
        
        # Парсим текущую страницу чтобы получить диапазон страниц
        start_page = Page.from_raw_url(url=TARGET_URL)
        await self.pages_queue.put(start_page)
        await PageParser.parse_content(start_page)

        # Постепенное добавление диапазона страниц в очередь
        for page_num in PageParser.get_pages_range(start_page):
            next_page = Page(
                url=start_page.url,
                page=page_num,
                query_data=start_page.query_data
            )
            await self.pages_queue.put(next_page)

        # Ожидание завершения всех задач
        await asyncio.gather(
            self.pages_queue.join(), 
            self.posts_queue.join(), 
            return_exceptions=True
        ) 

        # Завершение всех воркеров
        for w in workers:
            w.cancel()
        await asyncio.gather(*workers, return_exceptions=True)