"""add foreign-key to posts table

Revision ID: 0912cab9e88c
Revises: 02fc63c669ff
Create Date: 2023-02-01 09:40:32.349176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0912cab9e88c'
down_revision = '02fc63c669ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    # Master: referent_table + remote_cols
    # Table you want set the fk: source_table + local_cols
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'],
                           remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
