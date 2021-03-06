import base64
import json

import sentry_sdk
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from kokon import settings
from kokon.orm import User
from kokon.serializers import UserSchema
from kokon.utils.errors import AppError


def upsert_user_from_jwt(db, jwt_header_encoded):
    try:
        payload = json.loads(_base64_decode(jwt_header_encoded))
    except Exception as e:
        # We don't except this to happen, as right now auth happens before requests
        # hit the backend. Let's log to sentry.
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()
        raise AppError(message="Unauthorized.", status=401)

    assert "@" in payload["email"]
    authorized_emails = [i.strip() for i in settings.AUTHORIZED_EMAILS.split(",")]
    if not (
        payload["email"] in authorized_emails
        or f"*@{payload['email'].split('@')[-1]}" in authorized_emails
    ):
        raise AppError(message="Unauthorized.", status=401)

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
            insert(User)
            .values(user_dict)
            .on_conflict_do_update(index_elements=[User.google_sub], set_=user_dict)
        )
        session.execute(upsert_stmt)

        select_stmt = sa.select(User).where(User.google_sub == payload["sub"])
        user = session.execute(select_stmt).scalar()

        session.expunge_all()
        return user


# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/endpoints/getting-started/main.py#L35
def _base64_decode(encoded_str):
    # Add paddings manually if necessary.
    num_missed_paddings = 4 - len(encoded_str) % 4
    if num_missed_paddings != 4:
        encoded_str += "=" * num_missed_paddings
    return base64.urlsafe_b64decode(encoded_str).decode("utf-8")
