"""Module containing ORM."""

import uuid
import enum

import sqlalchemy.sql.functions as func

from sqlalchemy import Column, Integer, String, Enum, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Voivodeship(enum.Enum):
    """Class representing voivodeship enum in database."""

    GREATER_POL = "Greater Poland"
    KUYAVIA = "Kuyavia-Pomerania"
    LESSER_POL = "Lesser Poland"
    LODZ = "Łódź"
    LOWER_SIL = "Lower Silesia"
    LUBLIN = "Lublin"
    LUBUSZ = "Lubusz"
    MASOVIA = "Masovia"
    OPOLE = "Opole"
    PODLASKIE = "Podlaskie"
    POMERANIA = "Pomerania"
    SILESIA = "Silesia"
    SUBCARPATHIA = "Subcarpathia"
    HOLY_CROSS = "Holy Cross Province"
    WARMIA = "Warmia-Masuria"
    WEST_POM = "West Pomerania"


class ApartmentStatus(enum.Enum):
    """Class representing apartment status enum in database."""

    ADDED = "added"
    PHONE_VERIFIED = "phone_verified"
    IN_PERSON_VERIFIED = "in_person_verified"


# pylint: disable=too-few-public-methods
class Apartment(Base):
    """ORM for Apartments."""

    __tablename__ = ...

    id = Column("id", Integer, primary_key=True)
    guid = Column("guid", UUID(as_uuid=True), default=uuid.uuid4)
    created_at = Column("created_at", TIMESTAMP, server_default=func.now())
    updated_at = Column("updated_at", TIMESTAMP, onupdate=func.now())
    city = Column("city", String(50))
    zip = Column("zip", String(10), nullable=False)
    voivodeship = Column("voivodeship", Enum(Voivodeship))
    address_line = Column("address_line", String(512), nullable=False)
    vacancies_total = Column("vacancies_total", Integer, nullable=False)
    vacancies_free = Column("vacancies_free", Integer, nullable=False)
    have_pets = Column("have_pets", Boolean)
    accept_pets = Column("accept_pets", Boolean)
    comments = Column("comments", String(255))
    status = Column(
        "status", Enum(ApartmentStatus), default=ApartmentStatus.ADDED, nullable=False
    )

    def __repr__(self):
        return f"Apartment: {self.__dict__}"


class Host(Base):
    """ORM for Hosts."""

    __tablename__ = ...

    id = Column("id", Integer, primary_key=True)
    guid = Column("guid", UUID(as_uuid=True), default=uuid.uuid4)
    full_name = Column("full_name", String(256))
    email = Column("email", String(100))
    phone_number = Column("phone_number", String(20))
    call_after = Column("call_after", String(20), nullable=True)
    call_before = Column("call_before", String(20), nullable=True)
    comments = Column("comments", Text, nullable=True)
    created_at = Column("created_at", TIMESTAMP, server_default=func.now())
    updated_at = Column("updated_at", TIMESTAMP, onupdate=func.now())

    def __repr__(self):
        return f"Host: {self.__dict__}"
