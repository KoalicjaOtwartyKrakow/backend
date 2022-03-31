"""guests_claimed_by

Revision ID: 43f020236495
Revises: 8e8177b6e706
Create Date: 2022-03-22 14:24:13.692029

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "43f020236495"
down_revision = "8e8177b6e706"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "guests",
        sa.Column("claimed_by_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_guests_claimed_by_id", "guests", "users", ["claimed_by_id"], ["guid"]
    )


def downgrade():
    op.drop_constraint("fk_guests_claimed_by_id", "guests")
    op.drop_column("guests", "claimed_by_id")
