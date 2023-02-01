"""create posts table

Revision ID: 84413697022d
Revises: 
Create Date: 2023-01-17 08:33:02.143623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84413697022d'
down_revision = None
branch_labels = None
depends_on = None

# Run commands about the changes to database
def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                             sa.Column('title', sa.String(), nullable=False))
    pass

# Rollback function to go back to initial state
def downgrade() -> None:
    op.drop_table('posts')
    pass
