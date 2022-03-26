import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, TIMESTAMP, UUID as DB_UUID
from sqlalchemy.orm import relationship

from .base import Base
from .enums import GuestPriorityStatus, VerificationStatus


class Guest(Base):
    """ORM for Guests."""

    __versioned__ = {}
    __tablename__ = "guests"

    guid = sa.Column(
        "guid",
        DB_UUID(as_uuid=True),
        server_default=sa.text("uuid_generate_v4()"),
        primary_key=True,
    )
    full_name = sa.Column("full_name", sa.String(255), nullable=False)
    email = sa.Column("email", sa.String(255), nullable=False)
    phone_number = sa.Column("phone_number", sa.String(20), nullable=False)
    is_agent = sa.Column(
        "is_agent", sa.Boolean, server_default=sa.sql.expression.false(), nullable=False
    )
    document_number = sa.Column("document_number", sa.String(255))
    people_in_group = sa.Column(
        "people_in_group", sa.Integer, server_default=sa.text("1"), nullable=False
    )
    adult_male_count = sa.Column(
        "adult_male_count", sa.Integer, server_default=sa.text("0"), nullable=False
    )
    adult_female_count = sa.Column(
        "adult_female_count", sa.Integer, server_default=sa.text("0"), nullable=False
    )
    children_ages = sa.Column("children_ages", ARRAY(sa.Integer), nullable=False)
    have_pets = sa.Column(
        "have_pets",
        sa.Boolean,
        server_default=sa.sql.expression.false(),
        nullable=False,
    )
    pets_description = sa.Column("pets_description", sa.String(255))
    special_needs = sa.Column("special_needs", sa.Text)
    food_allergies = sa.Column("food_allergies", sa.Text)
    meat_free_diet = sa.Column(
        "meat_free_diet",
        sa.Boolean,
        server_default=sa.sql.expression.false(),
        nullable=False,
    )
    gluten_free_diet = sa.Column(
        "gluten_free_diet",
        sa.Boolean,
        server_default=sa.sql.expression.false(),
        nullable=False,
    )
    lactose_free_diet = sa.Column(
        "lactose_free_diet",
        sa.Boolean,
        server_default=sa.sql.expression.false(),
        nullable=False,
    )
    finance_status = sa.Column("finance_status", sa.String(255))
    how_long_to_stay = sa.Column("how_long_to_stay", sa.String(255))
    desired_destination = sa.Column("desired_destination", sa.String(255))
    priority_status = sa.Column(
        "priority_status", sa.Enum(GuestPriorityStatus), default=None
    )
    priority_date = sa.Column(
        "priority_date", TIMESTAMP(timezone=True), server_default=sa.func.now()
    )
    staff_comments = sa.Column("staff_comments", sa.Text)
    verification_status = sa.Column(
        "verification_status",
        sa.Enum(VerificationStatus),
        nullable=False,
        server_default=VerificationStatus.CREATED,
    )
    system_comments = sa.Column("system_comments", sa.Text, nullable=True)
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
    updated_by_id = sa.Column(
        "updated_by_id",
        sa.ForeignKey("users.guid", name="fk_guests_updated_by_id"),
        nullable=False,
    )
    updated_by = relationship(
        "User", back_populates="updated_guests", foreign_keys=[updated_by_id]
    )

    claimed_by_id = sa.Column(
        "claimed_by_id",
        sa.ForeignKey("users.guid", name="fk_guests_claimed_by_id"),
    )
    claimed_by = relationship(
        "User", back_populates="claimed_guests", foreign_keys=[claimed_by_id]
    )
    claimed_at = sa.Column(
        "claimed_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
    )

    accommodation_unit_id = sa.Column(
        "accommodation_unit_id",
        sa.ForeignKey("accommodation_units.guid", name="fk_accommodation_unit_id"),
    )
    accommodation_unit = relationship("AccommodationUnit", back_populates="guests")

    def __repr__(self):
        return f"Guest: {self.__dict__}"
