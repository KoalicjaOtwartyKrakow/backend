"""fiels_size_updates

Revision ID: b10c643435c4
Revises: 558b6e23830c
Create Date: 2022-03-31 13:26:29.859261

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "b10c643435c4"
down_revision = "558b6e23830c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "guests", "email", existing_type=sa.VARCHAR(length=255), nullable=True
    )

    op.alter_column(
        "accommodation_units",
        "city",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=250),
        existing_nullable=False,
    )
    op.alter_column(
        "accommodation_units_version",
        "city",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=250),
        existing_nullable=True,
    )

    op.execute(
        sa.text(
            """
            UPDATE guests SET updated_by_id = :user_guid WHERE updated_by_id IS NULL;
            """
        ).params(user_guid="28ab1bf2-f735-4603-b7f0-7938ba2ab059")
    )
    op.alter_column(
        "guests",
        "updated_by_id",
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "guests", "email", existing_type=sa.VARCHAR(length=255), nullable=False
    )

    op.alter_column(
        "accommodation_units",
        "city",
        existing_type=sa.VARCHAR(length=250),
        type_=sa.String(length=50),
        existing_nullable=False,
    )
    op.alter_column(
        "accommodation_units_version",
        "city",
        existing_type=sa.VARCHAR(length=250),
        type_=sa.String(length=50),
        existing_nullable=True,
    )
    # ### end Alembic commands ###
