from flask import current_app as app
from itsdangerous import URLSafeTimedSerializer

from dto import TokenPayload
from models.user import User
from repository.userRepository import userRepository


class TokenService:
    @staticmethod
    def generate(user: User) -> str:
        serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        payload = TokenPayload(publicId=user.publicId, isActive=user.isActive)
        token = serializer.dumps(payload, salt=app.config["SECURITY_PASSWORD_SALT"])
        return token

    @staticmethod
    def getPayload(token: str, expiration: int = 60 * 60 * 24) -> TokenPayload | None:
        try:
            serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
            return serializer.loads(
                token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
            )
        except Exception:
            return None

    @classmethod
    def verify(cls, token: str) -> User | None:
        try:
            payload: TokenPayload = cls.getPayload(token)
            if not payload:
                raise Exception
            user = userRepository.getByPublicId(payload["publicId"])
            if payload["isActive"] == user.isActive:
                return user
        except Exception:
            return None
