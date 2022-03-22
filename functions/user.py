import json

import flask
from sqlalchemy import select

from utils.db import acquire_db_session
from utils.orm import User
from utils.serializers import UserSchema, UUIDEncoder


def handle_get_all_users(_request):
    with acquire_db_session() as session:
        stmt = select(User)
        result = session.execute(stmt)
        user_schema = UserSchema()
        response = json.dumps(
            [user_schema.dump(g) for g in result.scalars()], cls=UUIDEncoder
        )
    return flask.Response(response=response, status=200, mimetype="application/json")

