"""Add column car_type to Cars model

Revision ID: 3e2b688bb17b
Revises: e45df29bbac3
Create Date: 2025-02-14 11:48:19.780801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e2b688bb17b'
down_revision = 'e45df29bbac3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cars', schema=None) as batch_op:
        batch_op.add_column(sa.Column('car_type', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cars', schema=None) as batch_op:
        batch_op.drop_column('car_type')

    # ### end Alembic commands ###
