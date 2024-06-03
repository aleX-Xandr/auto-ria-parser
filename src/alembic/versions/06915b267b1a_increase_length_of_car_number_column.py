"""Increase length of car_number column

Revision ID: 06915b267b1a
Revises: 9b767589df7a
Create Date: 2024-06-03 21:29:59.755377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06915b267b1a'
down_revision: Union[str, None] = '9b767589df7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('car_advertisements', 'car_number',
               existing_type=sa.VARCHAR(length=8),
               type_=sa.String(length=10),
               existing_nullable=False)


def downgrade():
    op.alter_column('car_advertisements', 'car_number',
               existing_type=sa.String(length=10),
               type_=sa.VARCHAR(length=8),
               existing_nullable=False)

