from sqlalchemy import select

from utils.functions import JSONResponse
from utils.orm import User
from utils.pagination import get_statement_pagination
from utils.serializers import UserSchema


def handle_get_all_users(request):
    with request.db.acquire() as session:
        stmt = select(User)
        pagination = get_statement_pagination(request, session, stmt)
        user_schema = UserSchema()
        response = [user_schema.dump(g) for g in pagination.items]

    return JSONResponse(response, status=200)
