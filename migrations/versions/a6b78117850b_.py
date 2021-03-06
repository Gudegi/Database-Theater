"""empty message

Revision ID: a6b78117850b
Revises: f0ed3b158f62
Create Date: 2021-11-30 20:53:15.365710

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a6b78117850b'
down_revision = 'f0ed3b158f62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notice_answer', sa.Column('question_id', sa.Integer(), nullable=True))
    op.drop_constraint('notice_answer_ibfk_1', 'notice_answer', type_='foreignkey')
    op.create_foreign_key(None, 'notice_answer', 'notice', ['question_id'], ['id'], ondelete='CASCADE')
    op.drop_column('notice_answer', 'notice_id')
    op.add_column('pay', sa.Column('discountpay', sa.Integer(), nullable=False))
    op.add_column('pay', sa.Column('lastpay', sa.Integer(), nullable=False))
    op.drop_column('pay', 'coupon_code')
    op.drop_column('pay', 'used_points')
    op.add_column('reservation', sa.Column('seat_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'reservation', 'seat', ['seat_id'], ['id'])
    op.drop_column('reservation', 'seats')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservation', sa.Column('seats', mysql.VARCHAR(length=1000), nullable=False))
    op.drop_constraint(None, 'reservation', type_='foreignkey')
    op.drop_column('reservation', 'seat_id')
    op.add_column('pay', sa.Column('used_points', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('pay', sa.Column('coupon_code', mysql.VARCHAR(length=20), nullable=False))
    op.drop_column('pay', 'lastpay')
    op.drop_column('pay', 'discountpay')
    op.add_column('notice_answer', sa.Column('notice_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'notice_answer', type_='foreignkey')
    op.create_foreign_key('notice_answer_ibfk_1', 'notice_answer', 'notice', ['notice_id'], ['id'], ondelete='CASCADE')
    op.drop_column('notice_answer', 'question_id')
    # ### end Alembic commands ###
