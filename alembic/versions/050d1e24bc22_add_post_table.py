"""add post table

Revision ID: 050d1e24bc22
Revises: 84027ce0b75a
Create Date: 2022-11-02 09:59:13.151146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '050d1e24bc22'
down_revision = '84027ce0b75a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key('post_users_fk',
                          source_table='posts',
                          referent_table='users',
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE'
                          )

    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
