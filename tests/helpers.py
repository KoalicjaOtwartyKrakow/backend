import os
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


class AppDB:
    """
    This db connection uses app user created in the app_role migration.
    """

    @contextmanager
    def acquire(self):
        session = sessionmaker(bind=self._pool())()

        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def _pool(self):
        return sa.create_engine(
            sa.engine.url.URL.create(
                drivername="postgresql+pg8000",
                username=os.getenv("db_app_user"),
                password=os.getenv("db_app_pass"),
                database=settings.DB_NAME,
                query=settings.DB_QUERY,
            ),
            pool_size=1,
            max_overflow=0,
        )
