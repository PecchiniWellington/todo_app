"""create posts table

Revision ID: b8d661bd314b
Revises: 
Create Date: 2022-10-27 09:58:31.001870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8d661bd314b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column("id", sa.Integer(),
                              primary_key=True,
                              nullable=False
                              ),
                    sa.Column("title", sa.String(), nullable=False),
                    sa.Column("description", sa.String(), nullable=False),
                    sa.Column("is_published", sa.Boolean(), nullable=False),
                    sa.Column("review", sa.Integer(), nullable=False),
                    sa.Column("create_at",
                              sa.TIMESTAMP(
                                  timezone=True
                              ),
                              nullable=False
                              ),
                    sa.Column("owner_id", sa.Integer(), nullable=False))

    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column(table_name='posts', column_name='owner_id')
    op.drop_table('posts')
    pass
