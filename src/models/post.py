import json
import logging
import re

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

from models.page import CarPage

Base = declarative_base()

class CarAdvertisement(Base):
    __tablename__ = "car_advertisements"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(128), nullable=False)
    title = Column(String(64), nullable=False)
    price_usd = Column(Float, nullable=False)
    odometer = Column(Integer, nullable=False)
    username = Column(String(64), nullable=False)
    phone_number = Column(String(16), nullable=False)
    image_url = Column(String(128), nullable=True)
    images_count = Column(Integer, nullable=False)
    car_number = Column(String(10), nullable=False)
    car_vin = Column(String(17), nullable=False)
    datetime_found = Column(DateTime, default=datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)

    # indices
    __table_args__ = (
        UniqueConstraint(
            "url",
            "title",
            "price_usd",
            "odometer",
            "username",
            "car_number",
            "car_vin",
            name="uix_url_title_price_odometer_user_carnum_carvin",
        ),
    )

    @staticmethod
    def price_from_html(page: CarPage, symbol: str = "$") -> int:
        to_int = lambda price_text: int(re.sub(r'\D', '', price_text))
        price_text = page.soup.find(True, {"class": "price_value"}).get_text()

        if symbol in price_text:
            return to_int(price_text)
        
        for price_tag in page.soup.find_all(True, {"class": "i-block"}):
            price_text = price_tag.get_text()
            if symbol in price_text:
                return to_int(price_text)
        else:
            return -1
        
    @staticmethod
    def price_from_json(offers: dict, page: CarPage, symbol: str = "USD") -> int:
        if offers["priceCurrency"] == symbol:
            return int(offers["price"])
        elif price_tag := page.soup.find("span", {"data-currency": symbol}):
            price_text = price_tag.get_text()
            return int(price_text.replace(" ", ""))
        elif price_tag := page.soup.find("script", {"data-currency": symbol}):
            return int(price_tag["data-seller-price"])
        
    @staticmethod
    def num_from_html(page: CarPage) -> str:
        car_num_tag = page.soup.find("span", {"class": "state-num ua"})
        if car_num_tag is not None:
            car_num_text = car_num_tag.get_text()
            pattern = r"[А-ЯA-Z]{2}\s+(\d{4})\s+[А-ЯA-Z]{2}"
            match = re.search(pattern, car_num_text)
            if match:
                return match.group()
        return ""
        
    @staticmethod
    def vin_from_html(page: CarPage) -> str:
        vin_tag = page.soup.find("span", {"class": "label-vin"})
        return "" if vin_tag is None else vin_tag.get_text()
        
    @classmethod
    def from_page(cls, page: CarPage) -> "CarAdvertisement":

        try:
            script_tag = page.soup.find("script", {"id": "ldJson2"})
            if script_tag is None:
                url = page.url
                title = page.soup.find(True, {"class": "auto-head_title"}).get_text()
                price_usd = cls.price_from_html(page)
                odometer = int() # TODO
            else:
                json_content = json.loads(script_tag.string)
                url = json_content["url"]
                title = json_content["name"]
                price_usd = cls.price_from_json(json_content["offers"], page)
                odometer = json_content["mileageFromOdometer"]["value"]

            car_num = cls.num_from_html(page)
            car_vin = cls.vin_from_html(page)
                
            username_tag = page.soup.find(True, {"class": "seller_info_name"})

            image_tag = page.soup.find("meta", {"property": "og:image"})

            images_tag = page.soup.find("div", {"class": "carousel-inner"})
            if images_tag is not None:        
                all_images = images_tag.find_all("div", {"class": "photo-620x465"})
            else:
                all_images = page.soup.find_all("div", {"class": "image-gallery-slide"})

            return cls(
                url = url,
                title = title,
                price_usd = price_usd,
                odometer = odometer,
                username = username_tag.get_text(),
                phone_number = "099 999 99 99", # TODO
                image_url = image_tag.get("content", ""), 
                images_count = len(all_images),
                car_number = car_num,
                car_vin = car_vin,            
            )
        except Exception as e:
            logging.error(e)