"""last22

Revision ID: 6ab38935b993
Revises: ee359f864cc5
Create Date: 2023-09-27 21:41:33.630276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ab38935b993'
down_revision: Union[str, None] = 'ee359f864cc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_id_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_id_key', 'users', ['id'])
    # ### end Alembic commands ###
