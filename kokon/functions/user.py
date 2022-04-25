from kokon.orm import User
from kokon.serializers import UserSchema
from kokon.utils.functions import JSONResponse
from kokon.utils.query import paginate


def handle_get_all_users(request):
    with request.db.acquire() as session:
        stmt = session.query(User)
        response = paginate(stmt, request=request, schema=UserSchema)

    return JSONResponse(response, status=200)
