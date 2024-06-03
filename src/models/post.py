import json
import re

from datetime import datetime, UTC
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
    car_number = Column(String(8), nullable=False)
    car_vin = Column(String(17), nullable=False)
    datetime_found = Column(DateTime, default=datetime.now(UTC), nullable=False)

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

    @classmethod
    def from_page(cls, page: CarPage) -> "CarAdvertisement":
        script_tag = page.soup.find("script", {"id": "ldJson2"})
        json_content = json.loads(script_tag.string)
        offers = json_content["offers"]

        if offers["priceCurrency"] != "USD":
            print("INVALID CURRENCY: ", offers)

        car_num_tag = page.soup.find("span", {"class": "state-num ua"})
        car_num_text = car_num_tag.get_text()
        pattern = r"[А-Я]{2}\s+(\d{4})\s+[А-Я]{2}"
        match = re.search(pattern, car_num_text)
        if match:
            car_num = match.group()
        else:
            car_num = ""
            print("INVALID STATE NUMBER: ", car_num_text)

        car_vin_tag = page.soup.find("span", {"class": "label-vin"})
        username_tag = page.soup.find("div", {"class": "seller_info_name bold"})
        image_tag = page.soup.find("meta", {"property": "og:image"})
        images_tag = page.soup.find("div", {"class": "carousel-inner"})
        all_images = images_tag.find_all("div", {"class": "photo-620x465"})

        return cls(
            url = json_content["url"],
            title = json_content["name"],
            price_usd = json_content["offers"]["price"],
            odometer = json_content["mileageFromOdometer"]["value"],
            username = username_tag.get_text(),
            phone_number = "099 999 99 99", # TODO
            image_url = image_tag.get("content", ""), 
            images_count = len(all_images),
            car_number = car_num,
            car_vin = car_vin_tag.get_text(),            
        )