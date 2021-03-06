import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID as DB_UUID
from sqlalchemy.orm import relationship

from .base import Base


class HostVerificationSession(Base):
    __tablename__ = "host_verification_sessions"

    id = sa.Column(
        "id",
        DB_UUID(as_uuid=True),
        server_default=sa.text("uuid_generate_v4()"),
        primary_key=True,
    )
    host_id = sa.Column(
        "host_id",
        sa.ForeignKey("hosts.guid", name="fk_host_verification_sessions_host_id"),
        nullable=False,
    )
    conversation_id = sa.Column(
        "conversation_id", sa.String(36), nullable=False, unique=True
    )
    first_name = sa.Column("first_name", sa.String(100), nullable=True)
    last_name = sa.Column("last_name", sa.String(100), nullable=True)
    phone_number = sa.Column("phone_number", sa.String(100), nullable=True)
    email = sa.Column("email", sa.String(100), nullable=True)
    url = sa.Column("url", sa.String(200), nullable=True)
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

    host = relationship("Host", back_populates="verifications", foreign_keys=[host_id])

    def __repr__(self):
        return f"HostVerificationSession: {self.__dict__}"
