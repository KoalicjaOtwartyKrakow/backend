"""Module containing ORM."""

import uuid

from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import declarative_base


Base = declarative_base()


# pylint: disable=too-few-public-methods
class Apartment(Base):
    """ORM for Apartments."""

    __tablename__ = ""

    id = Column("id", Integer, primary_key=True)
    guid = Column("guid", UUID(as_uuid=True), default=uuid.uuid4)
    created_at = Column("created_at", TIMESTAMP)
    update_at = Column("updated_at", TIMESTAMP)
