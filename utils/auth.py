import jwt

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

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
        user_dict = {
            "given_name": payload["given_name"],
            "family_name": payload["family_name"],
            "email": payload["email"],
            "google_sub": payload["sub"],
            "google_picture": payload["picture"],
        }

        # Pretty much for validation only, maybe we don't need that at all?
        UserSchema(camel_case=False).load(
            user_dict,
            session=session,
        )

        upsert_stmt = (
            insert(orm.User)
            .values(user_dict)
            .on_conflict_do_update(index_elements=[orm.User.google_sub], set_=user_dict)
        )
        session.execute(upsert_stmt)

        select_stmt = sa.select(orm.User).where(orm.User.google_sub == payload["sub"])
        user = session.execute(select_stmt).scalar()

        session.expunge_all()
        return user
