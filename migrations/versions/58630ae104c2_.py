"""empty message

Revision ID: 58630ae104c2
Revises: 
Create Date: 2022-11-14 14:20:54.208548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58630ae104c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descripcion', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todos')
    # ### end Alembic commands ###