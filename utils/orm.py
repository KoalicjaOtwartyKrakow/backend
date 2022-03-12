# pylint: disable=too-few-public-methods
"""Module containing ORM."""

import uuid
import enum
import json

import sqlalchemy.sql.functions as func

from sqlalchemy import Column, Integer, String, Enum, Boolean, Text, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, ARRAY
from sqlalchemy.orm import declarative_base, relationship


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


class Status(enum.Enum):
    """Class representing status enum in database."""

    CREATED = "created"
    VERIFIED = "verified"
    BANNED = "banned"

    def __str__(self):
        return self.name

# this will be useful in the future
# host_teammembers = Table('host_teammembers', Base.metadata,
#     Column('teammember_id', ForeignKey('teammembers.id'), primary_key=True),
#     Column('host_id', ForeignKey('hosts.id'), primary_key=True)
# )

host_languages = Table(
    "host_languages",
    Base.metadata,
    Column("language_code", ForeignKey("languages.code2")),
    Column("host_id", ForeignKey("hosts.id")),
    Column("id", Integer, primary_key=True),
)


class Host(Base):
    """ORM for Hosts."""

    __tablename__ = "hosts"

    id = Column("id", Integer, primary_key=True)
    guid = Column("guid", UUID(as_uuid=True), default=uuid.uuid4)
    full_name = Column("full_name", String(256))
    email = Column("email", String(100))
    phone_number = Column("phone_number", String(20))
    call_after = Column("call_after", String(64), nullable=True)
    call_before = Column("call_before", String(64), nullable=True)
    comments = Column("comments", Text, nullable=True)
    status = Column("status", Enum(Status), default=Status.CREATED)
    languages_spoken = relationship("Language", secondary=host_languages)
    created_at = Column("created_at", TIMESTAMP, server_default=func.now())
    updated_at = Column("updated_at", TIMESTAMP, onupdate=func.now())

    apartments = relationship("AccommodationUnit")

    def __repr__(self):
        return f"Host: {self.__dict__}"


class Voivodeship(enum.Enum):
    """Class representing voivodeship enum in database."""

    DOLNOSLASKIE = "DOLNOŚLĄSKIE"
    KUJAWSKOPOMORSKIE = "KUJAWSKO-POMORSKIE"
    LUBELSKIE = "LUBELSKIE"
    LUBUSKI = "LUBUSKIE"
    LODZKIE = "ŁÓDZKIE"
    MALOPOLSKIE = "MAŁOPOLSKIE"
    MAZOWIECKIE = "MAZOWIECKIE"
    OPOLSKIE = "OPOLSKIE"
    PODKARPACKIE = "PODKARPACKIE"
    PODLASKIE = "PODLASKIE"
    POMORSKIE = "POMORSKIE"
    SLASKIE = "ŚLĄSKIE"
    SWIETOKRZYSKIE = "ŚWIĘTOKRZYSKIE"
    WARMINSKOMAZURSKIE = "WARMIŃSKO-MAZURSKIE"
    WIELKOPOLSKIE = "WIELKOPOLSKIE"
    ZACHODNIOPOMORSKIE = "ZACHODNIOPOMORSKIE"


class AccommodationUnit(Base):
    """ORM for Apartments."""

    __tablename__ = "accommodation_units"

    id = Column("id", Integer, primary_key=True)
    guid = Column("guid", UUID(as_uuid=True), default=uuid.uuid4)
    created_at = Column("created_at", TIMESTAMP, server_default=func.now())
    updated_at = Column("updated_at", TIMESTAMP, onupdate=func.now())
    city = Column("city", String(50))
    zip = Column("zip", String(10), nullable=False)
    voivodeship = Column("voivodeship", Enum(Voivodeship))
    address_line = Column("address_line", String(512), nullable=False)
    vacancies_total = Column("vacancies_total", Integer, nullable=False)
    vacancies_free = Column("vacancies_free", Integer)
    have_pets = Column("have_pets", Boolean)
    accepts_pets = Column("accepts_pets", Boolean)
    comments = Column("comments", String(255))
    status = Column("status", Enum(Status), default=Status.CREATED, nullable=False)

    host_id = Column("host_id", ForeignKey("hosts.guid"))

    def __repr__(self):
        return f"Apartment: {self.__dict__}"

    def to_json(self):
        obj_dict = self.__dict__
        obj_dict.pop("__sa_instance_state")
        return json.dumps(dict, indent=4, sort_keys=True, default=str)


class LanguageEnum(enum.Enum):
    """Class representing language enum in database."""

    ENGLISH = "En"
    POLISH = "Pl"
    UKRAINIAN = "Uk"
    RUSSIAN = "Ru"


class Guest(Base):
    """ORM for Guests."""

    __tablename__ = "guests"

    id = Column("id", Integer, primary_key=True)
    guid = Column("guid", UUID(as_uuid=True), default=uuid.uuid4)
    full_name = Column("full_name", String(255))
    email = Column("email", String(100))
    phone_number = Column("phone_number", String(20))
    people_in_group = Column("people_in_group", Integer, default=1)
    adult_male_count = Column("adult_male_count", Integer)
    adult_female_count = Column("adult_female_count", Integer)
    children_count = Column("children_count", Integer)
    children_ages = Column("children_ages", ARRAY(Integer))
    have_pets = Column("have_pets", Boolean, nullable=True)
    pets_description = Column("pets_description", String(255), nullable=True)
    special_needs = Column("special_needs", Text, nullable=True)
    priority_date = Column("priority_date", TIMESTAMP, server_default=func.now())
    status = Column("status", Enum(Status), nullable=True, default=Status.CREATED)
    finance_status = Column("finance_status", String(255), nullable=True)
    how_long_to_stay = Column("how_long_to_stay", String(255), nullable=True)
    volunteer_note = Column("volunteer_note", Text, nullable=True)
    created_at = Column("created_at", TIMESTAMP, server_default=func.now())
    updated_at = Column("updated_at", TIMESTAMP, onupdate=func.now())

    def toJSON(self):
        dict = self.__dict__
        dict.pop('_sa_instance_state', None)
        return json.dumps(dict, indent=4, sort_keys=True, default=str)
