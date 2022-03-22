import jwt
import sqlalchemy as sa

from utils import settings, orm
from utils.serializers import UserSchema

from .base import BaseRepo


class UsersRepo(BaseRepo):
    def upsert_from_jwt(self, jwt_payload):
        try:
            payload = jwt.decode(jwt_payload, settings.JWT_SECRET, algorithms=["HS256"])
        except Exception:
            return None

        with self.db.acquire() as session:
            stmt = sa.select(orm.User).where(orm.User.google_sub == payload["sub"])
            user = session.execute(stmt).first()

            if user:
                return self.row_to_dict(user["User"])

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

            return self.row_to_dict(user)
