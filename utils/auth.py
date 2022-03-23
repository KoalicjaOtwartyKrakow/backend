import base64
import json

import sentry_sdk
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from utils import orm
from utils.serializers import UserSchema


def upsert_user_from_jwt(db, jwt_header_encoded):
    try:
        payload = json.loads(
            base64.urlsafe_b64decode(jwt_header_encoded).decode("utf-8")
        )
    except Exception as e:
        # We don't except this to happen, as right now auth happens before requests
        # hit the backend. Let's log to sentry.
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()
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
