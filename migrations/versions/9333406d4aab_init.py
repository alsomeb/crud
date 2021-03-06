"""init

Revision ID: 9333406d4aab
Revises: 
Create Date: 2022-01-12 19:51:16.955655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9333406d4aab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=80), nullable=False),
    sa.Column('lastname', sa.String(length=80), nullable=False),
    sa.Column('dob', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('year', sa.DateTime(), nullable=False),
    sa.Column('employeeId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['employeeId'], ['employee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicle')
    op.drop_table('employee')
    # ### end Alembic commands ###
