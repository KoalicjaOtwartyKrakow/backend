from sqlalchemy.orm import configure_mappers

from .accommodation_unit import AccommodationUnit
from .base import Base
from .guest import Guest
from .host import Host
from .language import Language
from .teammember import Teammember
from .user import User


__all__ = (
    "AccommodationUnit",
    "Base",
    "Guest",
    "Host",
    "Language",
    "Teammember",
    "User",
)


# https://sqlalchemy-continuum.readthedocs.io/en/latest/intro.html
configure_mappers()
