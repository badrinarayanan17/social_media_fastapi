"""add more columns to posts table

Revision ID: 5909d88825ad
Revises: 0e9dac2d3251
Create Date: 2023-05-29 14:37:21.687188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5909d88825ad'
down_revision = '0e9dac2d3251'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published'),
    op.drop_column('posts', 'created_at')
    pass
