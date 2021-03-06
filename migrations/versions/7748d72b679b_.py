"""empty message

Revision ID: 7748d72b679b
Revises: 656e743706a6
Create Date: 2021-11-19 23:51:04.188083

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7748d72b679b'
down_revision = '656e743706a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('benefit', 'benefit',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.Integer(),
               existing_nullable=False)
    op.alter_column('nonmember', 'birth_date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=False)
    op.alter_column('notice', 'content',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=True)
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
    op.alter_column('notice', 'content',
               existing_type=sa.String(length=255),
               type_=mysql.TEXT(),
               existing_nullable=True)
    op.alter_column('nonmember', 'birth_date',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=False)
    op.alter_column('benefit', 'benefit',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=20),
               existing_nullable=False)
    # ### end Alembic commands ###
