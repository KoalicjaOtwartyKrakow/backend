import os.path

from pytest import fixture

from tests.helpers import admin_session


def _setup_db():
    with admin_session() as session:
        assert session.bind.url.database.endswith("test")

        sql_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.sql")
        with open(sql_path) as f:
            session.execute(f.read())


@fixture
def db():
    _setup_db()
    yield
