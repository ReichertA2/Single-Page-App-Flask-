"""empty message

Revision ID: 0a855ac98b88
Revises: e45159aec0d7
Create Date: 2022-05-11 13:31:55.308927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a855ac98b88'
down_revision = 'e45159aec0d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('win_count', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('loss_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'loss_count')
    op.drop_column('user', 'win_count')
    # ### end Alembic commands ###