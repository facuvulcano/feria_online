"""empty message

Revision ID: b49f05353862
Revises: 86c8a3566c6b
Create Date: 2023-10-08 00:57:53.277922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b49f05353862'
down_revision = '86c8a3566c6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('brand_seller', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price_category', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('clothing_type', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('on_sale', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('brand_seller', schema=None) as batch_op:
        batch_op.drop_column('on_sale')
        batch_op.drop_column('clothing_type')
        batch_op.drop_column('price_category')

    # ### end Alembic commands ###