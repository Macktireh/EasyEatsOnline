from datetime import datetime
from typing import Type
from uuid import uuid4

from models.user import User
from repository.baseRepository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, model: Type[User]) -> None:
        super().__init__(model)

    def createSuperUser(self, *args, **kwargs) -> "User":
        super().create(isActive=True, isStaff=True, isAdmin=True, *args, **kwargs)

    def getByEmail(self, email: str) -> User | None:
        return self.model.query.filter_by(email=email).first()


userRepository = UserRepository(User)
