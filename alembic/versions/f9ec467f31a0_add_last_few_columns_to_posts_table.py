"""add last few columns to posts table

Revision ID: f9ec467f31a0
Revises: 0912cab9e88c
Create Date: 2023-02-01 09:58:31.798977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9ec467f31a0'
down_revision = '0912cab9e88c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
