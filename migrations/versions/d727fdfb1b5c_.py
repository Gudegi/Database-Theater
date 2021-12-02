"""empty message

Revision ID: d727fdfb1b5c
Revises: 86d2cffb076f
Create Date: 2021-11-08 12:00:00.030367

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd727fdfb1b5c'
down_revision = '86d2cffb076f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seattype',
    sa.Column('type', sa.String(length=10), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('type')
    )
    op.add_column('notice', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.drop_column('notice', 'number')
    op.add_column('reservation', sa.Column('seat_id', sa.Integer(), nullable=True))
    op.drop_constraint('reservation_ibfk_2', 'reservation', type_='foreignkey')
    op.create_foreign_key(None, 'reservation', 'seat', ['seat_id'], ['id'])
    op.drop_column('reservation', 'movie_id')
    op.drop_column('reservation', 'seat_number')
    op.add_column('screen', sa.Column('theater_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'screen', 'theater', ['theater_id'], ['id'])
    op.add_column('seat', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('seat', sa.Column('row', sa.String(length=1), nullable=False))
    op.add_column('seat', sa.Column('col', sa.Integer(), nullable=False))
    op.add_column('seat', sa.Column('seattype_type', sa.String(length=10), nullable=True))
    op.add_column('seat', sa.Column('seattype_price', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'seat', 'seattype', ['seattype_price'], ['price'])
    op.create_foreign_key(None, 'seat', 'seattype', ['seattype_type'], ['type'])
    op.drop_column('seat', 'type')
    op.drop_column('seat', 'number')
    op.drop_column('seat', 'seatprice')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seat', sa.Column('seatprice', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('seat', sa.Column('number', mysql.VARCHAR(length=10), nullable=False))
    op.add_column('seat', sa.Column('type', mysql.VARCHAR(length=20), nullable=False))
    op.drop_constraint(None, 'seat', type_='foreignkey')
    op.drop_constraint(None, 'seat', type_='foreignkey')
    op.drop_column('seat', 'seattype_price')
    op.drop_column('seat', 'seattype_type')
    op.drop_column('seat', 'col')
    op.drop_column('seat', 'row')
    op.drop_column('seat', 'id')
    op.drop_constraint(None, 'screen', type_='foreignkey')
    op.drop_column('screen', 'theater_id')
    op.add_column('reservation', sa.Column('seat_number', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('reservation', sa.Column('movie_id', mysql.VARCHAR(length=20), nullable=False))
    op.drop_constraint(None, 'reservation', type_='foreignkey')
    op.create_foreign_key('reservation_ibfk_2', 'reservation', 'seat', ['seat_number'], ['number'])
    op.drop_column('reservation', 'seat_id')
    op.add_column('notice', sa.Column('number', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False))
    op.drop_column('notice', 'id')
    op.drop_table('seattype')
    # ### end Alembic commands ###