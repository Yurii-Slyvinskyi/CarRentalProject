"""Add address to Users model

Revision ID: e45df29bbac3
Revises: c12a3e7a5930
Create Date: 2025-02-12 12:23:41.257450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e45df29bbac3'
down_revision = 'c12a3e7a5930'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(length=155), nullable=True))
        batch_op.add_column(sa.Column('address2', sa.String(length=155), nullable=True))
        batch_op.add_column(sa.Column('city', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('state', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('zip', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('zip')
        batch_op.drop_column('state')
        batch_op.drop_column('city')
        batch_op.drop_column('address2')
        batch_op.drop_column('address')

    # ### end Alembic commands ###
