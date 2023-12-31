"""initial migration

Revision ID: 86c8a3566c6b
Revises: 
Create Date: 2023-10-06 23:40:26.681210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86c8a3566c6b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand_seller',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('social_media', sa.String(length=120), nullable=True),
    sa.Column('proof_of_stock', sa.String(length=120), nullable=True),
    sa.Column('clothing_models', sa.String(length=120), nullable=True),
    sa.Column('approved', sa.Boolean(), nullable=True),
    sa.Column('notification', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('used_seller',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('social_media', sa.String(length=120), nullable=True),
    sa.Column('contact_number', sa.String(length=20), nullable=True),
    sa.Column('location', sa.String(length=120), nullable=True),
    sa.Column('number_of_items', sa.Integer(), nullable=True),
    sa.Column('approved', sa.Boolean(), nullable=True),
    sa.Column('notification', sa.Boolean(), nullable=True),
    sa.Column('items_sold', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('used_seller')
    op.drop_table('brand_seller')
    # ### end Alembic commands ###
