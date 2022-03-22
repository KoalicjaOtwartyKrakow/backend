import jwt

import sqlalchemy as sa

from utils import orm
from utils.serializers import UserSchema


def upsert_user_from_jwt(db, jwt_payload):
    try:
        payload = jwt.decode(
            jwt_payload,
            algorithms=["RS256"],
            # XXX(mlazowik): we do not validate the jwt, as it is already validated
            #  by cloud endpoints, before it reaches any backend functions. Makes
            #  tests and the temporarry mobile app api_key based access easier.
            #
            #  This _might_ not be the case when we switch to the proper auth flow.
            #  Remember to rethink this then.
            options={"verify_signature": False},
        )
    except Exception:
        return None

    with db.acquire() as session:
        stmt = sa.select(orm.User).where(orm.User.google_sub == payload["sub"])
        user = session.execute(stmt).first()

        if user:
            return user["User"].guid

        user = UserSchema().load(
            {
                "givenName": payload["given_name"],
                "familyName": payload["family_name"],
                "email": payload["email"],
                "googleSub": payload["sub"],
                "googlePicture": payload["picture"],
            },
            session=session,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        return user.guid
