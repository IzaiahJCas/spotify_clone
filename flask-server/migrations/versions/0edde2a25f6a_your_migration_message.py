"""Your migration message

Revision ID: 0edde2a25f6a
Revises: a010f3978649
Create Date: 2024-08-13 03:22:38.534940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0edde2a25f6a'
down_revision = 'a010f3978649'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('videos_included', schema=None) as batch_op:
        batch_op.drop_constraint('videos_included_file_name_key', type_='unique')
        batch_op.drop_constraint('videos_included_video_name_key', type_='unique')
        batch_op.drop_column('video_name')
        batch_op.drop_column('file_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('videos_included', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_name', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('video_name', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('videos_included_video_name_key', ['video_name'])
        batch_op.create_unique_constraint('videos_included_file_name_key', ['file_name'])

    # ### end Alembic commands ###
