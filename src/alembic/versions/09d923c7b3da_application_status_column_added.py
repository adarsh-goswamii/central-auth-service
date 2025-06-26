"""application status column added

Revision ID: 09d923c7b3da
Revises: c690119048d8
Create Date: 2025-06-26 15:12:18.436009
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '09d923c7b3da'
down_revision: Union[str, Sequence[str], None] = 'c690119048d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define enum type to match your model
application_status_enum = sa.Enum(
    'ACTIVE', 'INACTIVE', 'SUSPENDED',
    name='applicationstatus'
)

def upgrade() -> None:
    """Upgrade schema."""
    # Create enum type first
    application_status_enum.create(op.get_bind(), checkfirst=True)

    # Add the new column to the existing table
    op.add_column(
        'applications',
        sa.Column('status', application_status_enum, nullable=True),
        schema='auth'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('applications', 'status', schema='auth')
    application_status_enum.drop(op.get_bind(), checkfirst=True)
