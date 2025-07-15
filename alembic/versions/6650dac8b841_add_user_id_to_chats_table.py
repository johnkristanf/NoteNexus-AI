"""add user_id to chats table

Revision ID: 6650dac8b841
Revises: 8161ece08726
Create Date: 2025-07-15 15:12:35.920686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6650dac8b841'
down_revision: Union[str, Sequence[str], None] = '8161ece08726'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add user_id column to chats (as a normal column, no FK)."""
    op.add_column('chats', sa.Column('user_id', sa.String(), nullable=False))


def downgrade() -> None:
    """Remove user_id column from chats."""
    op.drop_column('chats', 'user_id')
