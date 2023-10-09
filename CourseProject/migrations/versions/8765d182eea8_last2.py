"""last2

Revision ID: 8765d182eea8
Revises: fd82dcbc030e
Create Date: 2023-09-23 19:09:06.628968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8765d182eea8'
down_revision: Union[str, None] = 'fd82dcbc030e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pictures', sa.Column('file_id', sa.String(), nullable=True))
    op.drop_column('pictures', 'url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pictures', sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('pictures', 'file_id')
    # ### end Alembic commands ###
