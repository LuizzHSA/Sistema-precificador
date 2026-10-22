"""Add persistent users and tenant ownership columns.

Revision ID: 0002_user_accounts
Revises: 0001_initial_schema
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_user_accounts"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    bind = op.get_bind()
    for table in ("stores", "products", "price_changes", "execution_logs", "audit_events"):
        if bind.dialect.name == "sqlite":
            # SQLite needs a batch table rebuild to add a foreign-key constraint.
            with op.batch_alter_table(table, recreate="always") as batch:
                batch.add_column(sa.Column("owner_id", sa.String(length=36), nullable=True))
                batch.create_foreign_key(
                    f"fk_{table}_owner_id_users", "users", ["owner_id"], ["id"]
                )
        else:
            op.add_column(table, sa.Column("owner_id", sa.String(length=36), nullable=True))
            op.create_foreign_key(
                f"fk_{table}_owner_id_users", table, "users", ["owner_id"], ["id"]
            )
        op.create_index(f"ix_{table}_owner_id", table, ["owner_id"])


def downgrade():
    for table in reversed(("stores", "products", "price_changes", "execution_logs", "audit_events")):
        op.drop_index(f"ix_{table}_owner_id", table_name=table)
        op.drop_constraint(f"fk_{table}_owner_id_users", table, type_="foreignkey")
        op.drop_column(table, "owner_id")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
