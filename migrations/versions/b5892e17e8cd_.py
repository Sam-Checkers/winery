"""empty message

Revision ID: b5892e17e8cd
Revises: b1ecb5f5b7ce
Create Date: 2024-03-05 10:54:02.657827

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b5892e17e8cd'
down_revision = 'b1ecb5f5b7ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wine', schema=None) as batch_op:
        batch_op.alter_column('type',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.String(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wine', schema=None) as batch_op:
        batch_op.alter_column('type',
               existing_type=sa.String(length=100),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)

    # ### end Alembic commands ###
