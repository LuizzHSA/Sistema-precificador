"""Make store email uniqueness tenant-specific.

Revision ID: 0004_tenant_store_email
Revises: 0003_user_token_version
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "0004_tenant_store_email"
down_revision = "0003_user_token_version"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    unique_constraints = inspector.get_unique_constraints("stores")
    email_constraints = [
        constraint for constraint in unique_constraints
        if constraint.get("column_names") == ["email"]
    ]

    if bind.dialect.name == "sqlite":
        with op.batch_alter_table(
            "stores",
            naming_convention={"uq": "uq_%(table_name)s_%(column_0_name)s"},
        ) as batch:
            for constraint in email_constraints:
                batch.drop_constraint(
                    constraint.get("name") or "uq_stores_email",
                    type_="unique",
                )
            batch.create_unique_constraint(
                "uq_store_owner_email", ["owner_id", "email"]
            )
    else:
        for constraint in email_constraints:
            if constraint.get("name"):
                op.drop_constraint(
                    constraint["name"], "stores", type_="unique"
                )
        op.create_unique_constraint(
            "uq_store_owner_email", "stores", ["owner_id", "email"]
        )


def downgrade():
    bind = op.get_bind()
    op.drop_constraint("uq_store_owner_email", "stores", type_="unique")
    op.create_unique_constraint("uq_stores_email", "stores", ["email"])
