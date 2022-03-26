from sqlalchemy import select

from kokon.utils.functions import JSONResponse
from kokon.orm import User
from kokon.serializers import UserSchema


def handle_get_all_users(request):
    with request.db.acquire() as session:
        stmt = select(User)
        result = session.execute(stmt)
        user_schema = UserSchema()
        response = [user_schema.dump(g) for g in result.scalars()]

    return JSONResponse(response, status=200)
