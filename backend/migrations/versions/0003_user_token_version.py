"""Add per-user JWT token version for logout revocation.

Revision ID: 0003_user_token_version
Revises: 0002_user_accounts
"""
from alembic import op
import sqlalchemy as sa

revision = "0003_user_token_version"
down_revision = "0002_user_accounts"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("token_version", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade():
    op.drop_column("users", "token_version")
