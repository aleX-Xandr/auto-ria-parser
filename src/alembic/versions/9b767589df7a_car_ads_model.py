"""car_ads_model

Revision ID: 9b767589df7a
Revises: 
Create Date: 2024-06-03 19:30:10.813880

"""
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b767589df7a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создание таблицы CarAdvertisement
    op.create_table(
        'car_advertisements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(length=128), nullable=False),
        sa.Column('title', sa.String(length=64), nullable=False),
        sa.Column('price_usd', sa.Float(), nullable=False),
        sa.Column('odometer', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=False),
        sa.Column('phone_number', sa.String(length=16), nullable=False),
        sa.Column('image_url', sa.String(length=128), nullable=True),
        sa.Column('images_count', sa.Integer(), nullable=False),
        sa.Column('car_number', sa.String(length=8), nullable=False),
        sa.Column('car_vin', sa.String(length=17), nullable=False),
        sa.Column('datetime_found', sa.DateTime(), nullable=False, default=datetime.now(timezone.utc)),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'url',
            'title',
            'price_usd',
            'odometer',
            'username',
            'car_number',
            'car_vin',
            name="uix_url_title_price_odometer_user_carnum_carvin"
        )
    )


def downgrade():
    # Удаление таблицы CarAdvertisement
    op.drop_table('car_advertisements')
