"""add table user

Revision ID: 65c3a448903d
Revises: 034969b74154
Create Date: 2023-11-03 11:08:57.209444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65c3a448903d'
down_revision: Union[str, None] = '034969b74154'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=75), nullable=True),
    sa.Column('language', sa.Enum('ARABIC', 'ENGLISH', name='applanguage'), nullable=False),
    sa.Column('is_staff', sa.Boolean(), nullable=False),
    sa.Column('date_joined', sa.DateTime(), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('is_locked', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__users'))
    )
    op.create_index(op.f('ix__users__email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix__users__email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
