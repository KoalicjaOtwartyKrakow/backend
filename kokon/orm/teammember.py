import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as DB_UUID

from .base import Base


class Teammember(Base):
    """ORM for Teammembers."""

    __tablename__ = "teammembers"

    guid = sa.Column(
        "guid",
        DB_UUID(as_uuid=True),
        server_default=sa.text("uuid_generate_v4()"),
        primary_key=True,
    )
    full_name = sa.Column("full_name", sa.String(100), nullable=True)
    phone_number = sa.Column("phone_number", sa.String(20), nullable=True)
