"""empty message

Revision ID: e1522dbd2f71
Revises: 7748d72b679b
Create Date: 2021-11-20 00:48:38.108658

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e1522dbd2f71'
down_revision = '7748d72b679b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pay', sa.Column('coupon_code', sa.String(length=20), nullable=False))
    op.add_column('pay', sa.Column('used_points', sa.Integer(), nullable=False))
    op.drop_column('pay', 'lastpay')
    op.drop_column('pay', 'discountpay')
    op.alter_column('review', 'rate',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.Float(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('review', 'rate',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)
    op.add_column('pay', sa.Column('discountpay', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('pay', sa.Column('lastpay', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_column('pay', 'used_points')
    op.drop_column('pay', 'coupon_code')
    # ### end Alembic commands ###
