import os.path

from pytest import fixture

from kokon.utils.db import DB


def _setup_db():
    with DB().acquire() as session:
        assert session.bind.url.database.endswith("test")

        sql_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.sql")
        with open(sql_path) as f:
            session.execute(f.read())


@fixture
def db():
    _setup_db()
    yield
