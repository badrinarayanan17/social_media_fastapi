"""add content column to posts table

Revision ID: b91ffac9cd71
Revises: 6be9382009f8
Create Date: 2023-05-29 14:01:12.534265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b91ffac9cd71'
down_revision = '6be9382009f8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(),nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts','content')
    pass
