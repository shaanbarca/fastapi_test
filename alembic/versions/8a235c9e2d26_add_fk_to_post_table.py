"""add fk to post table

Revision ID: 8a235c9e2d26
Revises: faa0c9e15019
Create Date: 2024-01-22 13:14:58.881693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a235c9e2d26'
down_revision: Union[str, None] = 'faa0c9e15019'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
