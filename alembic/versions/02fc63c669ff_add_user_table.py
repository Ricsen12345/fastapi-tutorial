"""add user table

Revision ID: 02fc63c669ff
Revises: 197c6ef65a65
Create Date: 2023-01-17 08:49:24.561857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02fc63c669ff'
down_revision = '197c6ef65a65'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
