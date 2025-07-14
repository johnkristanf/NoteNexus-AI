"""add notes table

Revision ID: fe3aeb220b91
Revises: 5ef498c61233
Create Date: 2025-07-13 11:23:05.288518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe3aeb220b91'
down_revision: Union[str, Sequence[str], None] = '5ef498c61233'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'notes',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('notes')
    # ### end Alembic commands ###
