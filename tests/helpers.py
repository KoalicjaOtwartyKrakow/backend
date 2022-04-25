from contextlib import contextmanager

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from kokon import settings


class UserMock:
    def __init__(self, guid):
        self.guid = guid

    def acquire(self):
        """Usage:
        with DB().acquire() as session:
            # use session here
        """


@contextmanager
def admin_session():
    """
    This creates a session for postgres user, not limited permissions.
    """
    pool = sa.create_engine(
        sa.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username="postgres",
            password=settings.DB_PASS,
            database=settings.DB_NAME,
            query=settings.DB_QUERY,
        ),
        pool_size=1,
        max_overflow=0,
    )

    session = sessionmaker(bind=pool)()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
