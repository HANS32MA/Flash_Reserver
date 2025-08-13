"""agregar campo video a posts

Revision ID: agregar_video_posts
Revises: f85b2d9d21f5
Create Date: 2025-01-08 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'agregar_video_posts'
down_revision = 'f85b2d9d21f5'
branch_labels = None
depends_on = None


def upgrade():
    # Agregar columna Video a la tabla posts
    op.add_column('posts', sa.Column('Video', sa.String(500), nullable=True))


def downgrade():
    # Remover columna Video de la tabla posts
    op.drop_column('posts', 'Video')
