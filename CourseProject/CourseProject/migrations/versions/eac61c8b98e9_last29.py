"""last29

Revision ID: eac61c8b98e9
Revises: fed934745b6c
Create Date: 2023-09-27 22:05:26.169537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eac61c8b98e9'
down_revision: Union[str, None] = 'fed934745b6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('next_post_id', sa.Integer(), nullable=True),
    sa.Column('prev_post_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('file_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feeling_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('feeling_id', sa.Integer(), nullable=True),
    sa.Column('feeling_str', sa.String(), nullable=True),
    sa.Column('describe', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['feeling_id'], ['feelings.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('next_post_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'posts', ['next_post_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'next_post_id')
    op.drop_table('feeling_logs')
    op.drop_table('photos')
    op.drop_table('posts')
    # ### end Alembic commands ###
