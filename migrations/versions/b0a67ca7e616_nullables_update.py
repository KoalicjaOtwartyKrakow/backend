"""nullables_update

Revision ID: b0a67ca7e616
Revises: cf53986008cf
Create Date: 2022-04-13 22:12:10.058866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b0a67ca7e616"
down_revision = "cf53986008cf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        f"""
    UPDATE accommodation_units SET city='' WHERE city IS NULL;
    UPDATE accommodation_units SET owner_comments='' WHERE owner_comments IS NULL;
    UPDATE accommodation_units SET staff_comments='' WHERE staff_comments IS NULL;
    UPDATE accommodation_units SET for_how_long='' WHERE for_how_long IS NULL;
    UPDATE accommodation_units SET system_comments='' WHERE system_comments IS NULL;
    UPDATE guests SET email='' WHERE email IS NULL;
    UPDATE guests SET document_number='' WHERE document_number IS NULL;
    UPDATE guests SET pets_description='' WHERE pets_description IS NULL;
    UPDATE guests SET special_needs='' WHERE special_needs IS NULL;
    UPDATE guests SET food_allergies='' WHERE food_allergies IS NULL;
    UPDATE guests SET finance_status='' WHERE finance_status IS NULL;
    UPDATE guests SET how_long_to_stay='' WHERE how_long_to_stay IS NULL;
    UPDATE guests SET desired_destination='' WHERE desired_destination IS NULL;
    UPDATE guests SET staff_comments='' WHERE staff_comments IS NULL;
    UPDATE guests SET system_comments='' WHERE system_comments IS NULL;
    UPDATE hosts SET call_after='' WHERE call_after IS NULL;
    UPDATE hosts SET call_before='' WHERE call_before IS NULL;
    UPDATE hosts SET comments='' WHERE comments IS NULL;
    UPDATE hosts SET system_comments='' WHERE system_comments IS NULL;
    """
    )

    op.alter_column(
        "accommodation_units",
        "city",
        existing_type=sa.VARCHAR(length=250),
        nullable=False,
    )
    op.alter_column(
        "accommodation_units", "owner_comments", existing_type=sa.TEXT(), nullable=False
    )
    op.alter_column(
        "accommodation_units", "staff_comments", existing_type=sa.TEXT(), nullable=False
    )
    op.alter_column(
        "accommodation_units",
        "for_how_long",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
    op.alter_column(
        "accommodation_units",
        "system_comments",
        existing_type=sa.TEXT(),
        nullable=False,
    )
    op.alter_column(
        "guests", "email", existing_type=sa.VARCHAR(length=255), nullable=False
    )
    op.alter_column(
        "guests",
        "document_number",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
    op.alter_column(
        "guests",
        "pets_description",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
    op.alter_column("guests", "special_needs", existing_type=sa.TEXT(), nullable=False)
    op.alter_column("guests", "food_allergies", existing_type=sa.TEXT(), nullable=False)
    op.alter_column(
        "guests", "finance_status", existing_type=sa.VARCHAR(length=255), nullable=False
    )
    op.alter_column(
        "guests",
        "how_long_to_stay",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
    op.alter_column(
        "guests",
        "desired_destination",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
    op.alter_column("guests", "staff_comments", existing_type=sa.TEXT(), nullable=False)
    op.alter_column(
        "guests", "system_comments", existing_type=sa.TEXT(), nullable=False
    )
    op.alter_column(
        "hosts", "call_after", existing_type=sa.VARCHAR(length=64), nullable=False
    )
    op.alter_column(
        "hosts", "call_before", existing_type=sa.VARCHAR(length=64), nullable=False
    )
    op.alter_column("hosts", "comments", existing_type=sa.TEXT(), nullable=False)
    op.alter_column("hosts", "system_comments", existing_type=sa.TEXT(), nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("hosts", "system_comments", existing_type=sa.TEXT(), nullable=True)
    op.alter_column("hosts", "comments", existing_type=sa.TEXT(), nullable=True)
    op.alter_column(
        "hosts", "call_before", existing_type=sa.VARCHAR(length=64), nullable=True
    )
    op.alter_column(
        "hosts", "call_after", existing_type=sa.VARCHAR(length=64), nullable=True
    )
    op.alter_column("guests", "system_comments", existing_type=sa.TEXT(), nullable=True)
    op.alter_column("guests", "staff_comments", existing_type=sa.TEXT(), nullable=True)
    op.alter_column(
        "guests",
        "desired_destination",
        existing_type=sa.VARCHAR(length=255),
        nullable=True,
    )
    op.alter_column(
        "guests",
        "how_long_to_stay",
        existing_type=sa.VARCHAR(length=255),
        nullable=True,
    )
    op.alter_column(
        "guests", "finance_status", existing_type=sa.VARCHAR(length=255), nullable=True
    )
    op.alter_column("guests", "food_allergies", existing_type=sa.TEXT(), nullable=True)
    op.alter_column("guests", "special_needs", existing_type=sa.TEXT(), nullable=True)
    op.alter_column(
        "guests",
        "pets_description",
        existing_type=sa.VARCHAR(length=255),
        nullable=True,
    )
    op.alter_column(
        "guests", "document_number", existing_type=sa.VARCHAR(length=255), nullable=True
    )
    op.alter_column(
        "guests", "email", existing_type=sa.VARCHAR(length=255), nullable=True
    )
    op.alter_column(
        "accommodation_units", "system_comments", existing_type=sa.TEXT(), nullable=True
    )
    op.alter_column(
        "accommodation_units",
        "for_how_long",
        existing_type=sa.VARCHAR(length=255),
        nullable=True,
    )
    op.alter_column(
        "accommodation_units", "staff_comments", existing_type=sa.TEXT(), nullable=True
    )
    op.alter_column(
        "accommodation_units", "owner_comments", existing_type=sa.TEXT(), nullable=True
    )
    op.alter_column(
        "accommodation_units",
        "city",
        existing_type=sa.VARCHAR(length=250),
        nullable=True,
    )
    # ### end Alembic commands ###
