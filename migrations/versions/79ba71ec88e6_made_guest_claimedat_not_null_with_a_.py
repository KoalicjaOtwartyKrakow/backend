"""Made Guest.claimedAt not null with a default

Revision ID: 79ba71ec88e6
Revises: afd7e4278146
Create Date: 2022-03-23 09:37:41.179007

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "79ba71ec88e6"
down_revision = "afd7e4278146"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    guests = sa.sql.table("guests", sa.Column("claimed_at", postgresql.TIMESTAMP()))
    op.execute(  # pylint: disable=no-member
        guests.update()
        .where(guests.c.claimed_at == None)  # noqa: E711
        .values(claimed_at=sa.text("now()"))
    )
    op.alter_column(  # pylint: disable=no-member
        "guests",
        "claimed_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(  # pylint: disable=no-member
        "guests",
        "claimed_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        nullable=True,
    )
    # ### end Alembic commands ###
