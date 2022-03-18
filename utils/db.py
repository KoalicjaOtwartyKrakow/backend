"""Module containing database connection."""

import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from .secret import access_secret_version


IS_LOCAL_DB = os.getenv("IS_LOCAL_DB", "False").lower() == "true"


def get_secret_var(name):
    if IS_LOCAL_DB:
        return os.getenv(name)

    return access_secret_version(name)


DB_USER = get_secret_var("db_user")
DB_PASS = get_secret_var("db_pass")
DB_NAME = get_secret_var("db_name")
DB_SOCKET_DIR = get_secret_var("db_socket_dir")
INSTANCE_CONNECTION_NAME = get_secret_var("instance_connection_name")
QUERY = (
    {"unix_sock": f"{DB_SOCKET_DIR}/{INSTANCE_CONNECTION_NAME}/.s.PGSQL.5432"}
    if not IS_LOCAL_DB
    else None
)


def get_engine():
    """Get database engine."""
    pool = sqlalchemy.create_engine(
        # See https://cloud.google.com/sql/docs/postgres/connect-functions#connect_to
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=DB_USER,  # e.g. "my-database-user"
            password=DB_PASS,  # e.g. "my-database-password"
            database=DB_NAME,  # e.g. "my-database-name"
            query=QUERY,
        )
    )
    print(f'Connecting to query={QUERY}, name={DB_NAME}')

    return pool


def get_db_session() -> sessionmaker:
    """Usage:
    ```
    Session = get_db_session()
    with Session() as session:
        # use session here
    """
    return sessionmaker(bind=get_engine())
