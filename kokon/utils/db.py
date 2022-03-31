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
                # See:
                # https://cloud.google.com/sql/docs/postgres/connect-functions#connect_to
                sqlalchemy.engine.url.URL.create(
                    drivername="postgresql+pg8000",
                    username=settings.DB_USER,  # e.g. "my-database-user"
                    password=settings.DB_PASS,  # e.g. "my-database-password"
                    database=settings.DB_NAME,  # e.g. "my-database-name"
                    query=settings.DB_QUERY,
                ),
                # Cloud SQL imposes a maximum limit on concurrent connections, and these
                # limits may vary depending on the database engine chosen (see Cloud SQL
                # Quotas and Limits). It's recommended to use a connection with Cloud
                # Functions, but it is important to set the maximum number of
                # connections to 1.
                #
                # Note: Cloud Functions limits concurrent executions to one per
                # instance. You never have a situation where a single function instance
                # is processing two requests at the same time. In most situations, only
                # a single database connection is needed.
                #
                # https://cloud.google.com/sql/docs/mysql/connect-functions#connection-limits
                pool_size=1,
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
