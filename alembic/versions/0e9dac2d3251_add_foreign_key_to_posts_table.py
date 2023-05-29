"""add foreign key to posts table

Revision ID: 0e9dac2d3251
Revises: 5d632fffc862
Create Date: 2023-05-29 14:30:12.849919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e9dac2d3251'
down_revision = '5d632fffc862'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk', source_table = 'posts', referent_table = 'users', local_cols = ['owner_id'], remote_cols = ['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
    pass
