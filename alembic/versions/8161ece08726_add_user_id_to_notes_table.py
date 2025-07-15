"""add user_id to notes table

Revision ID: 8161ece08726
Revises: fe3aeb220b91
Create Date: 2025-07-15 11:28:28.815730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8161ece08726'
down_revision: Union[str, Sequence[str], None] = 'fe3aeb220b91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add user_id column to notes (as a normal column, no FK)."""
    op.add_column('notes', sa.Column('user_id', sa.String(), nullable=False))


def downgrade() -> None:
    """Remove user_id column from notes."""
    op.drop_column('notes', 'user_id')