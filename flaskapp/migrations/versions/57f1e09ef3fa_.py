"""empty message

Revision ID: 57f1e09ef3fa
Revises: 4db3de09ceee
Create Date: 2024-01-13 12:12:29.286538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57f1e09ef3fa'
down_revision = '4db3de09ceee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pupils', schema=None) as batch_op:
        batch_op.drop_index('ix_pupils_tg_id')
        batch_op.create_index(batch_op.f('ix_pupils_tg_id'), ['tg_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pupils', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_pupils_tg_id'))
        batch_op.create_index('ix_pupils_tg_id', ['tg_id'], unique=False)

    # ### end Alembic commands ###