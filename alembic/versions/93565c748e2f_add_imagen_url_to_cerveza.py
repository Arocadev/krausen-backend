"""add imagen_url to cerveza
Revision ID: 93565c748e2f
Revises: 2753e9e5e0ab
Create Date: 2026-06-27 17:17:10.863971
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '93565c748e2f'
down_revision: Union[str, Sequence[str], None] = '2753e9e5e0ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('cervezas', sa.Column('imagen_url', sa.String(length=255), nullable=True))

def downgrade() -> None:
    op.drop_column('cervezas', 'imagen_url')
