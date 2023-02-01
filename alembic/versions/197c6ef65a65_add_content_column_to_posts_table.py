"""add content column to posts table

Revision ID: 197c6ef65a65
Revises: 84413697022d
Create Date: 2023-01-17 08:43:51.073874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '197c6ef65a65'
down_revision = '84413697022d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
