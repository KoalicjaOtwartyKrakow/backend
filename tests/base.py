from contextlib import contextmanager
from unittest import TestCase

from sqlalchemy import event


class BaseTestCase(TestCase):
    def setUp(self):
        self.db = Gateways.database_rw()
        connection = self.db._engine.connect()
        self._transaction = connection.begin()

    @contextmanager
    def session(self):
        with self.db.session() as session:
            # start the session in a SAVEPOINT...
            session._session.begin_nested()

            @event.listens_for(session._session, "after_transaction_end")
            def restart_savepoint(sqlalchemy_session, transaction):
                if transaction.nested and not transaction._parent.nested:

                    # ensure that state is expired the way
                    # session.commit() at the top level normally does
                    # (optional step)
                    sqlalchemy_session.expire_all()

                    sqlalchemy_session.begin_nested()

            yield session

    def tearDown(self):
        self._transaction.rollback()
