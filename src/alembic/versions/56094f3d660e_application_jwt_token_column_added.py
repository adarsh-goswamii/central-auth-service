"""application jwt token column added

Revision ID: 56094f3d660e
Revises: 09d923c7b3da
Create Date: 2025-07-09 08:42:41.403152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56094f3d660e'
down_revision: Union[str, Sequence[str], None] = '09d923c7b3da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add JWT key columns to applications table."""
    op.add_column('applications', sa.Column('private_key', sa.Text(), nullable=True), schema='auth')
    op.add_column('applications', sa.Column('public_key', sa.Text(), nullable=True), schema='auth')


def downgrade() -> None:
    """Remove JWT key columns from applications table."""
    op.drop_column('applications', 'public_key', schema='auth')
    op.drop_column('applications', 'private_key', schema='auth')
