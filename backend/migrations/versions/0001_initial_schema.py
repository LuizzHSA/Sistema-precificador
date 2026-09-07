"""Create the initial application schema.

Revision ID: 0001_initial_schema
Revises:
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    existing_tables = set(inspect(bind).get_table_names())

    if "stores" not in existing_tables:
        op.create_table(
            "stores",
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("name", sa.String(length=120), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("phone", sa.String(length=40), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email"),
        )

    if "products" not in existing_tables:
        op.create_table(
            "products",
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("store_id", sa.String(length=36), nullable=False),
            sa.Column("name", sa.String(length=160), nullable=False),
            sa.Column("sku", sa.String(length=80), nullable=False),
            sa.Column("current_price", sa.Float(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["store_id"], ["stores.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("store_id", "sku", name="uq_product_store_sku"),
        )

    if "price_changes" not in existing_tables:
        op.create_table(
            "price_changes",
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("store_id", sa.String(length=36), nullable=False),
            sa.Column("product_id", sa.String(length=36), nullable=False),
            sa.Column("current_price", sa.Float(), nullable=False),
            sa.Column("new_price", sa.Float(), nullable=False),
            sa.Column("effective_date", sa.DateTime(), nullable=False),
            sa.Column("status", sa.String(length=20), nullable=False),
            sa.Column("reason", sa.String(length=500), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.Column("executed_at", sa.DateTime(), nullable=True),
            sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
            sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
            sa.ForeignKeyConstraint(["store_id"], ["stores.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
    elif "retry_count" not in {column["name"] for column in inspect(bind).get_columns("price_changes")}:
        op.add_column("price_changes", sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"))

    if "execution_logs" not in existing_tables:
        op.create_table(
            "execution_logs",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("price_change_id", sa.String(length=36), nullable=False),
            sa.Column("status", sa.String(length=20), nullable=False),
            sa.Column("message", sa.String(length=1000), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["price_change_id"], ["price_changes.id"]),
            sa.PrimaryKeyConstraint("id"),
        )

    if "audit_events" not in existing_tables:
        op.create_table(
            "audit_events",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("action", sa.String(length=120), nullable=False),
            sa.Column("entity_type", sa.String(length=80), nullable=False),
            sa.Column("entity_id", sa.String(length=120), nullable=False),
            sa.Column("payload", sa.JSON(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )

    inspector = inspect(bind)
    indexes = {
        (table, index["name"])
        for table in inspector.get_table_names()
        for index in inspector.get_indexes(table)
    }
    for table, name, columns in (
        ("products", "ix_products_store_id", ["store_id"]),
        ("products", "ix_products_sku", ["sku"]),
        ("price_changes", "ix_price_changes_store_id", ["store_id"]),
        ("price_changes", "ix_price_changes_product_id", ["product_id"]),
        ("price_changes", "ix_price_changes_status", ["status"]),
        ("execution_logs", "ix_execution_logs_price_change_id", ["price_change_id"]),
        ("execution_logs", "ix_execution_logs_created_at", ["created_at"]),
        ("audit_events", "ix_audit_events_action", ["action"]),
        ("audit_events", "ix_audit_events_entity_id", ["entity_id"]),
        ("audit_events", "ix_audit_events_created_at", ["created_at"]),
    ):
        if (table, name) not in indexes:
            op.create_index(name, table, columns)


def downgrade():
    op.drop_table("audit_events")
    op.drop_table("execution_logs")
    op.drop_table("price_changes")
    op.drop_table("products")
    op.drop_table("stores")
