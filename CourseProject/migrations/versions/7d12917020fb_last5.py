"""last5

Revision ID: 7d12917020fb
Revises: 15376d1e4220
Create Date: 2023-09-24 13:27:06.005510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d12917020fb'
down_revision: Union[str, None] = '15376d1e4220'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('id_last_post', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'id_last_post')
    # ### end Alembic commands ###
