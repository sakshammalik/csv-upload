"""empty message

Revision ID: a1b9aef2d08d
Revises: 
Create Date: 2019-06-19 14:49:16.933568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b9aef2d08d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('sku', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('sku')
    )
    op.create_index(op.f('ix_products_sku'), 'products', ['sku'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_products_sku'), table_name='products')
    op.drop_table('products')
    # ### end Alembic commands ###
