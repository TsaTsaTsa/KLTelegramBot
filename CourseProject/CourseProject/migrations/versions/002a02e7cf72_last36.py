"""last36

Revision ID: 002a02e7cf72
Revises: d527b2a7b600
Create Date: 2023-10-07 11:34:57.445107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002a02e7cf72'
down_revision: Union[str, None] = 'd527b2a7b600'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercise_logs', sa.Column('is_done_last_month', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exercise_logs', 'is_done_last_month')
    # ### end Alembic commands ###
