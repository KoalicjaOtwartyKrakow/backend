# pylint: disable=too-few-public-methods
"""Module containing ORM."""

import uuid
import enum

import sqlalchemy.sql.functions as func

from sqlalchemy import Column, Integer, String, Enum, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, ARRAY
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Teammember(Base):
    """ORM for Teammembers."""

    __tablename__ = "teammembers"

    id = Column("id", Integer, primary_key=True)
    guid = Column("guid", UUID(as_uuid=True), default=uuid.uuid4)
    full_name = Column("full_name", String(20), nullable=True)
    phone_number = Column("phone_number", String(20), nullable=True)


class Language(Base):
    """ORM for Languages."""

    __tablename__ = "languages"

    name = Column("name", String(20))
    code2 = Column("code2", String(2), primary_key=True)
    code3 = Column("code3", String(3))


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


class LanguageEnum(enum.Enum):
    """Class representing language enum in database."""

    ENGLISH = "En"
    POLISH = "Pl"
    UKRAINIAN = "Uk"
    RUSSIAN = "Ru"


class HostStatus(enum.Enum):
    """Class representing host status enum in database."""

    CREATED = "created"
    VERIFIED = "verified"
    REJECTED = "rejected"


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
    languages_spoken = Column("languages_spoken", ARRAY(LanguageEnum), nullable=True)
    status = Column("status")
    created_at = Column("created_at", TIMESTAMP, server_default=func.now())
    updated_at = Column("updated_at", TIMESTAMP, onupdate=func.now())

    def __repr__(self):
        return f"Host: {self.__dict__}"


class Guest(Base):
    """ORM for Guests."""

    __tablename__ = ...

    id = Column("id", Integer, primary_key=True)
    guid = Column("guid", UUID(as_uuid=True), default=uuid.uuid4)
    full_name = Column("full_name", String(255))
    phone_number = Column("phone_number", String(20))
    people_in_group = Column("people_in_group", Integer, default=1)
    adult_man_count = Column("adult_man_count", Integer)
    adult_women_count = Column("adult_women_count", Integer)
    children_count = Column("children_count", Integer)
    children_ages = Column("children_ages", ARRAY)
    have_pets = Column("have_pets", Boolean, nullable=True)
    pets_description = Column("pets_description", String(255), nullable=True)
    special_needs = Column("special_needs", Text, nullable=True)
    priority_date = Column("priority_date", TIMESTAMP, server_default=func.now())
    status = Column("status", Integer, nullable=True)
    finance_status = Column("finance_status", String(255), nullable=True)
    stay_length = Column("stay_length", String(255), nullable=True)
    volunteer_note = Column("volunteer_note", Text, nullable=True)
    created_at = Column("created_at", TIMESTAMP, server_default=func.now())
    updated_at = Column("updated_at", TIMESTAMP, onupdate=func.now())
