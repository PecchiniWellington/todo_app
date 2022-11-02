"""add time stamp now and server default in published

Revision ID: bbc683b5c123
Revises: 050d1e24bc22
Create Date: 2022-11-02 11:03:03.775447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbc683b5c123'
down_revision = '050d1e24bc22'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('posts', "create_at",
                    server_default=sa.text('NOW()'),
                    )
    op.alter_column('posts', "is_published",  server_default='TRUE')

    pass


def downgrade() -> None:
    op.alter_column('posts', "is_published", sa.Boolean(), nullable=False),
    op.alter_column('posts', "create_at",
              sa.TIMESTAMP(
                  timezone=True
              ),
              nullable=False
              ),
    pass
