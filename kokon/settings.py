import os


IS_LOCAL_DB = os.getenv("IS_LOCAL_DB", "False").lower() == "true"


DB_USER = os.getenv("db_user", default="app_user")
DB_PASS = os.getenv("db_pass", default="postgres")
DB_NAME = os.getenv("db_name", default="kokon_dev")
DB_SOCKET_DIR = os.getenv("db_socket_dir")
INSTANCE_CONNECTION_NAME = os.getenv("instance_connection_name")

DB_QUERY = (
    {"unix_sock": f"{DB_SOCKET_DIR}/{INSTANCE_CONNECTION_NAME}/.s.PGSQL.5432"}
    if not IS_LOCAL_DB
    else None
)

SENTRY_DSN = os.getenv("sentry_dsn")
SENTRY_TRACES_SAMPLE_RATE = os.getenv("sentry_traces_sample_rate", 0)

AUTHORIZED_EMAILS = os.getenv("authorized_emails", "*@example.com,*@example.com")

AUTHOLOGIC_URL = os.getenv("authologic_url", default="")
AUTHOLOGIC_USER = os.getenv("authologic_user")
AUTHOLOGIC_PASS = os.getenv("authologic_pass")
