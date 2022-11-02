"""add user table

Revision ID: 84027ce0b75a
Revises: b8d661bd314b
Create Date: 2022-11-02 09:42:26.626432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84027ce0b75a'
down_revision = 'b8d661bd314b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',
                              sa.Integer(),
                              nullable=False,
                              primary_key=True,
                              ),
                    sa.Column('email',
                              sa.String(),
                              nullable=False,
                              unique=True
                              ),
                    sa.Column('password',
                              sa.String(),
                              nullable=False
                              ),
                    sa.Column('create_at',
                              sa.TIMESTAMP(timezone=True),
                              nullable=False,
                              server_default=sa.text('now()'),
                              ),
                    ),
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
