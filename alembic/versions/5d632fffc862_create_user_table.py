"""create user table

Revision ID: 5d632fffc862
Revises: b91ffac9cd71
Create Date: 2023-05-29 14:05:54.922326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d632fffc862'
down_revision = 'b91ffac9cd71'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer(),primary_key=True,nullable=True),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
                    sa.UniqueConstraint('email')
                    
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
