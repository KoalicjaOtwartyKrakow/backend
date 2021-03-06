import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as DB_UUID, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import Base
from .enums import VerificationStatus, Voivodeship, WorkflowStatus


class AccommodationUnit(Base):
    """ORM for Apartments."""

    __versioned__ = {}
    __tablename__ = "accommodation_units"

    guid = sa.Column(
        "guid",
        DB_UUID(as_uuid=True),
        server_default=sa.text("uuid_generate_v4()"),
        primary_key=True,
    )
    host_id = sa.Column(
        "host_id",
        sa.ForeignKey("hosts.guid", name="fk_host"),
        nullable=False,
        index=True,
    )
    city = sa.Column("city", sa.String(250), server_default=sa.text(""), nullable=False)
    zip = sa.Column("zip", sa.String(10), nullable=False)
    voivodeship = sa.Column("voivodeship", sa.Enum(Voivodeship))
    address_line = sa.Column("address_line", sa.String(512), nullable=False)
    vacancies_total = sa.Column("vacancies_total", sa.Integer, nullable=False)
    pets_present = sa.Column("pets_present", sa.Boolean)
    pets_accepted = sa.Column("pets_accepted", sa.Boolean)
    disabled_people_friendly = sa.Column("disabled_people_friendly", sa.Boolean)
    lgbt_friendly = sa.Column("lgbt_friendly", sa.Boolean)
    parking_place_available = sa.Column("parking_place_available", sa.Boolean)
    owner_comments = sa.Column(
        "owner_comments", sa.Text, server_default=sa.text(""), nullable=False
    )
    easy_ambulance_access = sa.Column("easy_ambulance_access", sa.Boolean)
    vacancies_free = sa.Column("vacancies_free", sa.Integer)
    staff_comments = sa.Column(
        "staff_comments", sa.Text, server_default=sa.text(""), nullable=False
    )
    verification_status = sa.Column(
        "verification_status",
        sa.Enum(VerificationStatus),
        server_default=VerificationStatus.CREATED,
        nullable=False,
    )
    workflow_status = sa.Column(
        "workflow_status",
        sa.Enum(WorkflowStatus),
        server_default=WorkflowStatus.NEEDS_VERIFICATION,
        nullable=False,
    )
    for_how_long = sa.Column(
        "for_how_long", sa.String(255), server_default=sa.text(""), nullable=False
    )
    system_comments = sa.Column(
        "system_comments", sa.Text, server_default=sa.text(""), nullable=False
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

    host = relationship("Host", back_populates="accommodation_units")
    guests = relationship("Guest", back_populates="accommodation_unit")

    def __repr__(self):
        return f"AccommodationUnit: {self.__dict__}"
