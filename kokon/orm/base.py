from sqlalchemy.orm import declarative_base
from sqlalchemy_continuum import make_versioned


__all__ = ("Base",)


Base = declarative_base()


make_versioned(user_cls=None, options={"native_versioning": True})
