"""Module containing ORM."""

import uuid
import enum

import sqlalchemy.sql.functions as func

from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class VoivodeshipEnum(enum.Enum):
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


# pylint: disable=too-few-public-methods
class Apartment(Base):
    """ORM for Apartments."""

    __tablename__ = ""

    id = Column("id", Integer, primary_key=True)
    guid = Column("guid", UUID(as_uuid=True), default=uuid.uuid4)
    created_at = Column("created_at", TIMESTAMP, server_default=func.now())
    updated_at = Column("updated_at", TIMESTAMP, onupdate=func.now())
    city = Column("city", String(50))
    zip = Column("zip", String(10), nullable=False)
    voivodeship = Column("voivodeship", Enum(VoivodeshipEnum))
    address_line = Column("address_line", String(512), nullable=False)
    vacancies_total = Column("vacancies_total", Integer, nullable=False)
    vacancies_free = Column("vacancies_free", Integer, nullable=False)
    have_pets = Column("have_pets", Boolean)
    accept_pets = Column("accept_pets", Boolean)
    comments = Column("comments", String(255))
    status = Column("status", Enum(), default=..., nullable=False)
