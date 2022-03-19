# pylint: disable=too-few-public-methods
"""Module containing ORM."""

import uuid
import enum
import json
from datetime import datetime, date

import sqlalchemy.sql.functions as func

from sqlalchemy import Column, Integer, String, Enum, Boolean, Text, Table, ForeignKey
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.dialects.postgresql import UUID as DB_UUID, TIMESTAMP, ARRAY
from sqlalchemy.orm import declarative_base, relationship, registry

Base = declarative_base()


class Teammember(Base):
    """ORM for Teammembers."""

    __tablename__ = "teammembers"

    id = Column("id", Integer, primary_key=True)
    guid = Column("guid", DB_UUID(as_uuid=True), default=uuid.uuid4)
    full_name = Column("full_name", String(20), nullable=True)
    phone_number = Column("phone_number", String(20), nullable=True)


class Language(Base):
    """ORM for Languages."""

    __tablename__ = "languages"

    name = Column("name", String(20))
    code2 = Column("code2", String(2), primary_key=True)
    code3 = Column("code3", String(3))


# https://stackoverflow.com/a/51976841
class Status(str, enum.Enum):
    """Class representing status enum in database."""

    CREATED = "created"
    VERIFIED = "verified"
    REJECTED = "rejected"

    def __str__(self):
        return self.value


# https://stackoverflow.com/a/51976841
class PriorityStatus(str, enum.Enum):
    """Class representing status enum in database."""

    DOES_NOT_RESPOND = "does_not_respond"
    ACCOMMODATION_NOT_NEEDED = "accommodation_not_needed"
    EN_ROUTE_UA = "en_route_ua"
    EN_ROUTE_PL = "en_route_pl"
    IN_KRK = "in_krk"
    AT_R3 = "at_r3"
    ACCOMMODATION_FOUND = "accommodation_found"
    UPDATED = "updated"

    def __str__(self):
        return self.value


# this will be useful in the future
# host_teammembers = Table('host_teammembers', Base.metadata,
#     Column('teammember_id', ForeignKey('teammembers.id'), primary_key=True),
#     Column('host_id', ForeignKey('hosts.id'), primary_key=True)
# )

host_languages = Table(
    "host_languages",
    Base.metadata,
    Column("language_code", ForeignKey("languages.code2")),
    Column("host_id", ForeignKey("hosts.guid")),
    Column("id", Integer, primary_key=True),
)


class Host(Base):
    """ORM for Hosts."""

    __tablename__ = "hosts"

    id = Column("id", Integer, primary_key=True)
    guid = Column("guid", DB_UUID(as_uuid=True), default=uuid.uuid4)
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


# https://stackoverflow.com/a/51976841
class Voivodeship(str, enum.Enum):
    """Class representing voivodeship enum in database."""

    DOLNOSLASKIE = "DOLNOŚLĄSKIE"
    KUJAWSKOPOMORSKIE = "KUJAWSKO-POMORSKIE"
    LUBELSKIE = "LUBELSKIE"
    LUBUSKIE = "LUBUSKIE"
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
    guid = Column("guid", DB_UUID(as_uuid=True), default=uuid.uuid4)
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
    disabled_people_friendly = Column("disabled_people_friendly", Boolean)
    lgbt_friendly = Column("lgbt_friendly", Boolean)
    parking_place_available = Column("parking_place_available", Boolean)
    easy_ambulance_access = Column("easy_ambulance_access", Boolean)
    owner_comments = Column("owner_comments", String(255))
    staff_comments = Column("staff_comments", String(255))
    status = Column("status", Enum(Status), default=Status.CREATED, nullable=False)

    host_id = Column("host_id", ForeignKey("hosts.guid"))

    host = relationship("Host")
    guests = relationship("Guest", back_populates="accommodation")

    def __repr__(self):
        return f"Apartment: {self.__dict__}"


class LanguageEnum(enum.Enum):
    """Class representing language enum in database."""

    ENGLISH = "En"
    POLISH = "Pl"
    UKRAINIAN = "Uk"
    RUSSIAN = "Ru"


# #TODO: implementation does not match api.yaml "GuestCreate:"
class Guest(Base):
    """ORM for Guests."""

    __tablename__ = "guests"

    id = Column("id", Integer, primary_key=True)
    guid = Column("guid", DB_UUID(as_uuid=True), default=uuid.uuid4)
    full_name = Column("full_name", String(255))
    email = Column("email", String(255))
    phone_number = Column("phone_number", String(20))
    is_agent = Column("is_agent", Boolean, default=False)
    document_number = Column("document_number", String(255), nullable=True)
    people_in_group = Column("people_in_group", Integer, default=1)
    adult_male_count = Column("adult_male_count", Integer, default=0)
    adult_female_count = Column("adult_female_count", Integer, default=0)
    children_count = Column("children_count", Integer, default=0)
    children_ages = Column("children_ages", ARRAY(Integer), nullable=True)
    have_pets = Column("have_pets", Boolean, nullable=True)
    pets_description = Column("pets_description", String(255), nullable=True)
    special_needs = Column("special_needs", Text, nullable=True)
    priority_date = Column("priority_date", TIMESTAMP, server_default=func.now())
    status = Column("status", Enum(Status), nullable=True, default=Status.CREATED)
    priority_status = Column(
        "priority_status", Enum(PriorityStatus), nullable=True, default=None
    )
    finance_status = Column("finance_status", String(255), nullable=True)
    how_long_to_stay = Column("how_long_to_stay", String(255), nullable=True)
    preferred_location = Column("preferred_location", String(255), nullable=True)
    volunteer_note = Column("volunteer_note", Text, nullable=True)
    validation_notes = Column("validation_notes", Text, nullable=True)
    created_at = Column("created_at", TIMESTAMP, server_default=func.now())
    updated_at = Column("updated_at", TIMESTAMP, onupdate=func.now())

    accommodation_unit_id = Column(
        "accommodation_unit_id", ForeignKey("accommodation_units.guid")
    )
    accommodation = relationship("AccommodationUnit", back_populates="guests")

    def __repr__(self):
        return f"Guest: {self.__dict__}"


# https://stackoverflow.com/a/19053800/526604
def to_camel_case(s):
    components = s.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


do_not_expand_list = {
    "AccommodationUnit": ["guests"],
    "Guest": ["accommodationUnit"],
    "Host": ["apartments"],
}


# https://stackoverflow.com/a/10664192
def new_alchemy_encoder(root_class):
    _visited_objs = []
    root_class_name = root_class.__class__.__name__

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            try:
                if isinstance(obj.__class__, DeclarativeMeta):
                    # don't re-visit self
                    if obj.__class__.__name__ != "Language" and obj in _visited_objs:
                        return None
                    _visited_objs.append(obj)

                    # an SQLAlchemy class
                    fields = {}

                    def is_circular_ref_field(name):
                        class_name = obj.__class__.__name__
                        if root_class_name != class_name:
                            return name in do_not_expand_list.get(class_name, [])
                        return False

                    for field in [
                        x
                        for x in dir(obj)
                        if not x.startswith("_")
                        and x != "metadata"
                        and x != "registry"
                        and not is_circular_ref_field(x)
                    ]:
                        camel_field = to_camel_case(field)
                        fields[camel_field] = obj.__getattribute__(field)
                    # a json-encodable dict
                    return fields

                if isinstance(obj, (datetime, date)):
                    return obj.isoformat()

                if isinstance(obj, uuid.UUID):
                    return obj.hex

                if isinstance(obj, registry):
                    return None
            except Exception:
                print("Exception!!")
                print(obj)
                raise

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder
