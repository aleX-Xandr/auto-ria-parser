from typing import Any

from components.base import BaseParser, BaseWorker
from models.page import CarPost


class PostParser(BaseParser):
    @staticmethod
    def get_data(page: CarPost) -> Any:
        ... # TODO
    

class PostWorker(BaseWorker):
    processor: PostParser = PostParser