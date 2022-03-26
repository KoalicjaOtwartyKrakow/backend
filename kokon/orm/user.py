import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as DB_UUID
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    """ORM for Users."""

    __tablename__ = "users"

    guid = sa.Column(
        "guid",
        DB_UUID(as_uuid=True),
        server_default=sa.text("uuid_generate_v4()"),
        primary_key=True,
    )
    given_name = sa.Column("given_name", sa.String(100), nullable=False)
    family_name = sa.Column("family_name", sa.String(100), nullable=False)
    email = sa.Column("email", sa.String(255), nullable=False, unique=True)
    google_sub = sa.Column("google_sub", sa.String(255), nullable=False, unique=True)
    google_picture = sa.Column("google_picture", sa.String(255), nullable=False)
    claimed_guests = relationship(
        "Guest", back_populates="claimed_by", foreign_keys="[Guest.claimed_by_id]"
    )
    updated_guests = relationship(
        "Guest", back_populates="updated_by", foreign_keys="[Guest.updated_by_id]"
    )

    def __repr__(self):
        return f"User: {self.__dict__}"
