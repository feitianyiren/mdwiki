"""empty message

Revision ID: 92d8727bbbb5
Revises: 8645016bd6da
Create Date: 2016-11-19 02:00:08.712500

"""

# revision identifiers, used by Alembic.
revision = '92d8727bbbb5'
down_revision = '8645016bd6da'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_post_old_20161115')
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('createAt', sa.DateTime(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['username'])

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('createAt')

    op.create_table('_post_old_20161115',
    sa.Column('location', sa.INTEGER(), nullable=False),
    sa.Column('userId', sa.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('location')
    )
    ### end Alembic commands ###
