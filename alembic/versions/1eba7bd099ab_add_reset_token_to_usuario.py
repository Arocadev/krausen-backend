"""add reset token to usuario
Revision ID: 1eba7bd099ab
Revises: 2148b004426d
Create Date: 2026-06-28 01:33:03.178888
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '1eba7bd099ab'
down_revision: Union[str, Sequence[str], None] = '2148b004426d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('usuarios', sa.Column('reset_token', sa.String(length=100), nullable=True))
    op.add_column('usuarios', sa.Column('reset_token_expira', sa.DateTime(), nullable=True))

def downgrade() -> None:
    op.drop_column('usuarios', 'reset_token_expira')
    op.drop_column('usuarios', 'reset_token')