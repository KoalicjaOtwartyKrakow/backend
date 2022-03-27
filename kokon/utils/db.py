"""Module containing database connection."""
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from kokon import settings


class DB:

    _db_connection_pool = None

    @classmethod
    def _get_db_connection_pool(cls):
        """Get database engine."""
        if cls._db_connection_pool is None:
            cls._db_connection_pool = sqlalchemy.create_engine(
                # See https://cloud.google.com/sql/docs/postgres/connect-functions#connect_to
                sqlalchemy.engine.url.URL.create(
                    drivername="postgresql+pg8000",
                    username=settings.DB_USER,  # e.g. "my-database-user"
                    password=settings.DB_PASS,  # e.g. "my-database-password"
                    database=settings.DB_NAME,  # e.g. "my-database-name"
                    query=settings.DB_QUERY,
                ),
                pool_size=5,
                max_overflow=0,
            )
            print(f"Connecting to query={settings.DB_QUERY}, name={settings.DB_NAME}")

        return cls._db_connection_pool

    @contextmanager
    def acquire(self):
        """Usage:
        with DB().acquire() as session:
            # use session here
        """
        session = sessionmaker(bind=self._get_db_connection_pool())()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
