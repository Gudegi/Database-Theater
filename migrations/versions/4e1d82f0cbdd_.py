"""empty message

Revision ID: 4e1d82f0cbdd
Revises: 48551da36cce
Create Date: 2021-11-11 23:40:48.038849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e1d82f0cbdd'
down_revision = '48551da36cce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pay',
    sa.Column('number', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('firstpay', sa.Integer(), nullable=False),
    sa.Column('discountpay', sa.Integer(), nullable=False),
    sa.Column('lastpay', sa.Integer(), nullable=False),
    sa.Column('method', sa.String(length=20), nullable=False),
    sa.Column('reservation_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['reservation_id'], ['reservation.id'], ),
    sa.PrimaryKeyConstraint('number')
    )
    op.create_table('cancel',
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('cancelpay', sa.Integer(), nullable=False),
    sa.Column('usingcoupon', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('pay_number', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pay_number'], ['pay.number'], ),
    sa.PrimaryKeyConstraint('number')
    )
    op.create_table('discount',
    sa.Column('member_id', sa.String(length=20), nullable=False),
    sa.Column('pay_number', sa.Integer(), nullable=False),
    sa.Column('pay_reservation_id', sa.Integer(), nullable=False),
    sa.Column('discount_amount', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.ForeignKeyConstraint(['pay_number'], ['pay.number'], ),
    sa.ForeignKeyConstraint(['pay_reservation_id'], ['pay.reservation_id'], ),
    sa.PrimaryKeyConstraint('member_id', 'pay_number', 'pay_reservation_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('discount')
    op.drop_table('cancel')
    op.drop_table('pay')
    # ### end Alembic commands ###
