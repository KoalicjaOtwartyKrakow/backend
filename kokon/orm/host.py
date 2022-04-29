import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as DB_UUID, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import Base
from .enums import VerificationStatus


# this will be useful in the future
# host_teammembers = Table('host_teammembers', Base.metadata,
#     Column('teammember_id', ForeignKey('teammembers.id'), primary_key=True),
#     Column('host_id', ForeignKey('hosts.id'), primary_key=True)
# )


host_languages = sa.Table(
    "host_languages",
    Base.metadata,
    sa.Column("language_code", sa.ForeignKey("languages.code2", name="fk_language")),
    sa.Column(
        "host_id",
        sa.ForeignKey("hosts.guid", name="fk_host", ondelete="CASCADE"),
        index=True,
    ),
    sa.Column(
        "guid",
        DB_UUID(as_uuid=True),
        server_default=sa.text("uuid_generate_v4()"),
        primary_key=True,
    ),
    sa.UniqueConstraint("language_code", "host_id", name="lang_host_pair_unique"),
)


class Host(Base):
    """ORM for Hosts."""

    __tablename__ = "hosts"

    guid = sa.Column(
        "guid",
        DB_UUID(as_uuid=True),
        server_default=sa.text("uuid_generate_v4()"),
        primary_key=True,
    )
    full_name = sa.Column("full_name", sa.String(256), nullable=False)
    email = sa.Column("email", sa.String(100), nullable=False)
    phone_number = sa.Column("phone_number", sa.String(20), nullable=False)
    call_after = sa.Column(
        "call_after", sa.String(64), server_default=sa.text(""), nullable=False
    )
    call_before = sa.Column(
        "call_before", sa.String(64), server_default=sa.text(""), nullable=False
    )
    comments = sa.Column(
        "comments", sa.Text, server_default=sa.text(""), nullable=False
    )
    languages_spoken = relationship("Language", secondary=host_languages)
    status = sa.Column(
        "status",
        sa.Enum(VerificationStatus),
        nullable=False,
        server_default=VerificationStatus.CREATED,
    )
    created_at = sa.Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
    )
    updated_at = sa.Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
    system_comments = sa.Column(
        "system_comments", sa.Text, server_default=sa.text(""), nullable=False
    )

    accommodation_units = relationship("AccommodationUnit", back_populates="host")
    verifications = relationship("HostVerificationSession", back_populates="host")

    def __repr__(self):
        return f"Host: {self.__dict__}"
