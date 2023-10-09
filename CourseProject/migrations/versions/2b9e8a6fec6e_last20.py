"""last20

Revision ID: 2b9e8a6fec6e
Revises: 49bc15fc621b
Create Date: 2023-09-27 21:40:41.579444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2b9e8a6fec6e'
down_revision: Union[str, None] = '49bc15fc621b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feeling_logs')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feeling_logs',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('feeling_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('feeling_str', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('describe', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['feeling_id'], ['feelings.id'], name='feeling_logs_feeling_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='feeling_logs_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='feeling_logs_pkey')
    )
    # ### end Alembic commands ###
