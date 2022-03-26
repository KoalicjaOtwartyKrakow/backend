import sqlalchemy as sa

from .base import Base


class Language(Base):
    """ORM for Languages."""

    __tablename__ = "languages"

    name = sa.Column("name", sa.String(20))
    code2 = sa.Column("code2", sa.String(2), primary_key=True)
    code3 = sa.Column("code3", sa.String(3))
