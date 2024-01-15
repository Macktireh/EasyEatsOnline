from typing import Any, Dict

from flask import current_app as app
from itsdangerous import URLSafeTimedSerializer

from models.user import User
from repositories.userRepository import userRepository
from utils.types import TokenPayload


class TokenService:
    @staticmethod
    def generate(payload: Dict[str, Any]) -> str:
        serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        token = serializer.dumps(payload, salt=app.config["SECURITY_PASSWORD_SALT"])
        return token

    @staticmethod
    def getPayload(token: str, expiration: int) -> TokenPayload | None:
        try:
            serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
            payload = serializer.loads(token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration)
            return payload
        except Exception:
            return None

    @classmethod
    def verify(cls, token: str, expiration: int = 60 * 60 * 24) -> User | None:
        try:
            payload = cls.getPayload(token, expiration)
            if not payload:
                raise Exception
            user = userRepository.getByPublicId(payload["publicId"])
            if payload["isActive"] == user.isActive:
                return user
        except Exception:
            return None
