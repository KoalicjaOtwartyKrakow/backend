import os

from .secret import access_secret_version_or_none


IS_LOCAL_DB = os.getenv("IS_LOCAL_DB", "False").lower() == "true"


def get_secret_var(name, default=None):
    if IS_LOCAL_DB:
        return os.getenv(name, default)

    return access_secret_version_or_none(name)


DB_USER = get_secret_var("db_user", default="postgres")
DB_PASS = get_secret_var("db_pass", default="postgres")
DB_NAME = get_secret_var("db_name", default="kokon_dev")
DB_SOCKET_DIR = get_secret_var("db_socket_dir")
INSTANCE_CONNECTION_NAME = get_secret_var("instance_connection_name")

DB_QUERY = (
    {"unix_sock": f"{DB_SOCKET_DIR}/{INSTANCE_CONNECTION_NAME}/.s.PGSQL.5432"}
    if not IS_LOCAL_DB
    else None
)

JWT_SECRET = get_secret_var("jwt_secret", default="secret")
