"""empty message

Revision ID: be3ebe1ded28
Revises: 5a671b80c1cd
Create Date: 2021-11-08 13:34:07.582851

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'be3ebe1ded28'
down_revision = '5a671b80c1cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('info')
    op.add_column('commute', sa.Column('user_id', sa.String(length=20), nullable=True))
    op.create_foreign_key(None, 'commute', 'user', ['user_id'], ['id'])
    op.add_column('evaluation', sa.Column('user_id', sa.String(length=20), nullable=True))
    op.create_foreign_key(None, 'evaluation', 'user', ['user_id'], ['id'])
    op.add_column('schedulemanage', sa.Column('user_id', sa.String(length=20), nullable=True))
    op.create_foreign_key(None, 'schedulemanage', 'user', ['user_id'], ['id'])
    op.add_column('user', sa.Column('gender', sa.String(length=10), nullable=False))
    op.add_column('user', sa.Column('birth_date', sa.Date(), nullable=False))
    op.add_column('user', sa.Column('age', sa.Integer(), nullable=False))
    op.add_column('user', sa.Column('phone', sa.String(length=11), nullable=False))
    op.add_column('user', sa.Column('salary', sa.Integer(), nullable=False))
    op.add_column('user', sa.Column('account', sa.String(length=20), nullable=False))
    op.add_column('user', sa.Column('department_info', sa.String(length=20), nullable=True))
    op.add_column('user', sa.Column('theater_id', sa.String(length=20), nullable=True))
    op.create_foreign_key(None, 'user', 'theater', ['theater_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'theater_id')
    op.drop_column('user', 'department_info')
    op.drop_column('user', 'account')
    op.drop_column('user', 'salary')
    op.drop_column('user', 'phone')
    op.drop_column('user', 'age')
    op.drop_column('user', 'birth_date')
    op.drop_column('user', 'gender')
    op.drop_constraint(None, 'schedulemanage', type_='foreignkey')
    op.drop_column('schedulemanage', 'user_id')
    op.drop_constraint(None, 'evaluation', type_='foreignkey')
    op.drop_column('evaluation', 'user_id')
    op.drop_constraint(None, 'commute', type_='foreignkey')
    op.drop_column('commute', 'user_id')
    op.create_table('info',
    sa.Column('department', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('position', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('authority', mysql.VARCHAR(length=20), nullable=True),
    sa.PrimaryKeyConstraint('department', 'position'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
