from datetime import datetime, UTC
from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class CarListing(Base):
    __tablename__ = 'car_listings'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(128), nullable=False)
    title = Column(String(64), nullable=False)
    price_usd = Column(Float(), nullable=False)
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