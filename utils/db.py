"""Module containing database connection."""

import sqlalchemy

from .secret import access_secret_version


DB_USER = access_secret_version("db_user")
DB_PASS = access_secret_version("db_pass")
DB_NAME = access_secret_version("db_name")
DB_HOST = access_secret_version("db_host")
DB_SOCKET_DIR = access_secret_version("db_socket_dir")
INSTANCE_CONNECTION_NAME = access_secret_version("instance_connection_name")


def get_engine():
    """Get database engine."""
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername="postgres+pg8000",
            username=DB_USER,  # e.g. "my-database-user"
            password=DB_PASS,  # e.g. "my-database-password"
            database=DB_NAME,  # e.g. "my-database-name"
            query={"unix_socket": f"{DB_SOCKET_DIR}/{INSTANCE_CONNECTION_NAME}"},
        )
    )

    return pool
