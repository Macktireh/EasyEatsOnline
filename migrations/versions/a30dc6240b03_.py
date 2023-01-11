"""empty message

Revision ID: a30dc6240b03
Revises: 8e468ec508e2
Create Date: 2023-01-07 19:33:19.470900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a30dc6240b03'
down_revision = '8e468ec508e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('createdAt', sa.DateTime(), nullable=False))
        batch_op.drop_column('createAt')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('createAt', sa.DATETIME(), nullable=False))
        batch_op.drop_column('createdAt')

    # ### end Alembic commands ###