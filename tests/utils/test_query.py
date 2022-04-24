from unittest.mock import Mock

from kokon.orm import AccommodationUnit, User
from kokon.serializers import UserSchema
from kokon.utils.query import filter_stmt, paginate, sort_stmt
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

        # TODO(nanvel): for backward compatibility, return later
        request = Mock(args={})
        result = paginate(stmt, request=request, schema=UserSchema)
        assert [i["email"] for i in result] == [
            "jane.doe@example.com",
            "john.doe@example.com",
        ]


def test_filter_stmt(db):
    with DB().acquire() as session:
        stmt = session.query(AccommodationUnit)

        # enum
        request = Mock(args={"verificationStatus": "REJECTED"})
        result = filter_stmt(stmt, request=request, model=AccommodationUnit).all()
        assert len(result) == 0

        # string
        request = Mock(args={"city": "Lublin"})
        result = filter_stmt(stmt, request=request, model=AccommodationUnit).all()
        assert len(result) == 1

        request = Mock(args={"city": "~Lub"})
        result = filter_stmt(stmt, request=request, model=AccommodationUnit).all()
        assert len(result) == 1

        request = Mock(args={"city": "NotKnown"})
        result = filter_stmt(stmt, request=request, model=AccommodationUnit).all()
        assert len(result) == 0

        # boolean
        request = Mock(args={"petsPresent": "true"})
        result = filter_stmt(stmt, request=request, model=AccommodationUnit).all()
        assert len(result) == 0

        # integer
        request = Mock(args={"vacanciesFree": "5"})
        result = filter_stmt(stmt, request=request, model=AccommodationUnit).all()
        assert len(result) == 1

        request = Mock(args={"vacanciesFreeLt": "2"})
        result = filter_stmt(stmt, request=request, model=AccommodationUnit).all()
        assert len(result) == 0

        request = Mock(args={"vacanciesFreeGte": "2"})
        result = filter_stmt(stmt, request=request, model=AccommodationUnit).all()
        assert len(result) == 1

        # dates
        request = Mock(args={"createdAtGt": "1999-01-01"})
        result = filter_stmt(stmt, request=request, model=AccommodationUnit).all()
        assert len(result) == 1


def test_sort_stmt(db):
    with DB().acquire() as session:
        stmt = session.query(User)
        request = Mock(args={"sort": "email"})
        result = sort_stmt(stmt, request=request, model=User).first()
        assert result.email == "jane.doe@example.com"

        request = Mock(args={"sort": "-email"})
        result = sort_stmt(stmt, request=request, model=User).first()
        assert result.email == "john.doe@example.com"
