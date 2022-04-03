from unittest.mock import Mock

from kokon.orm import User
from kokon.serializers import UserSchema
from kokon.utils.pagination import paginate
from kokon.utils.db import DB


def test_paginate(db):
    with DB().acquire() as session:
        stmt = session.query(User).order_by("email")

        request = Mock(args={"offset": 0, "limit": 1})
        result = paginate(stmt, request=request, schema=UserSchema)
        result["items"] = [i["email"] for i in result["items"]]

        assert result == {"items": ["jane.doe@example.com"], "total": 2}

        request = Mock(args={"offset": 1, "limit": 1})
        result = paginate(stmt, request=request, schema=UserSchema)
        result["items"] = [i["email"] for i in result["items"]]

        assert result == {"items": ["john.doe@example.com"], "total": 2}
