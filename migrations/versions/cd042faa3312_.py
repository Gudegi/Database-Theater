"""empty message

Revision ID: cd042faa3312
Revises: fbefa02d614f
Create Date: 2021-11-20 01:08:37.348677

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cd042faa3312'
down_revision = 'fbefa02d614f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservation', sa.Column('seats', sa.String(length=1000), nullable=False))
    op.drop_constraint('reservation_ibfk_4', 'reservation', type_='foreignkey')
    op.drop_column('reservation', 'seat_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservation', sa.Column('seat_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('reservation_ibfk_4', 'reservation', 'seat', ['seat_id'], ['id'])
    op.drop_column('reservation', 'seats')
    # ### end Alembic commands ###