"""conversation_unique_id_add_url

Revision ID: 8e712308ae1f
Revises: 757371c2ab60
Create Date: 2022-05-04 17:26:31.305369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8e712308ae1f"
down_revision = "757371c2ab60"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(  # pylint: disable=no-member
        "host_verification_sessions",
        sa.Column("url", sa.String(length=200), nullable=True),
    )
    op.add_column(  # pylint: disable=no-member
        "host_verification_sessions",
        sa.Column("phone_number", sa.String(length=200), nullable=True),
    )
    op.add_column(  # pylint: disable=no-member
        "host_verification_sessions",
        sa.Column("email", sa.String(length=200), nullable=True),
    )
    op.create_unique_constraint(  # pylint: disable=no-member
        "host_verification_sessions_conversation_id_key",
        "host_verification_sessions",
        ["conversation_id"],
    )


def downgrade():
    op.drop_constraint(  # pylint: disable=no-member
        "host_verification_sessions_conversation_id_key",
        "host_verification_sessions",
        type_="unique",
    )
    op.drop_column("host_verification_sessions", "url")  # pylint: disable=no-member
    op.drop_column(  # pylint: disable=no-member
        "host_verification_sessions", "phone_number"
    )
    op.drop_column("host_verification_sessions", "email")  # pylint: disable=no-member
