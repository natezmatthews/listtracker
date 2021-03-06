"""empty message

Revision ID: 09b1bce5d8aa
Revises: 
Create Date: 2018-02-10 15:12:26.063497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09b1bce5d8aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('risuto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=280), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_risuto_name'), 'risuto', ['name'], unique=False)
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item', sa.String(length=80), nullable=True),
    sa.Column('risuto_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['risuto_id'], ['risuto.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('separator',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator', sa.String(length=5), nullable=True),
    sa.Column('risuto_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['risuto_id'], ['risuto.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('separator')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('separator')
    op.drop_table('item')
    op.drop_index(op.f('ix_risuto_name'), table_name='risuto')
    op.drop_table('risuto')
    # ### end Alembic commands ###
