from kokon.orm import User
from kokon.serializers import UserSchema
from kokon.utils.functions import JSONResponse


def handle_get_all_users(request):
    with request.db.acquire() as session:
        result = session.query(User).all()
        response = UserSchema().dump(result, many=True)

    return JSONResponse(response, status=200)
