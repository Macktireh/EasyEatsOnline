from typing import List

from werkzeug import exceptions

from dto import RequestUserUpdateDTO
from models.user import User
from repository.userRepository import userRepository


class UserService:
    @staticmethod
    def getAllUser() -> List[User]:
        return userRepository.getAll()

    @staticmethod
    def getUser(publicId: str) -> User:
        user: User | None = userRepository.getByPublicId(publicId)
        if not user:
            raise exceptions.NotFound("User not found")
        return user

    @staticmethod
    def updateUser(publicId: str, data: RequestUserUpdateDTO) -> User:
        user = userRepository.getByPublicId(publicId)
        if not user:
            raise exceptions.NotFound("User not found")

        user.firstName = data.get("firstName", user.firstName)
        user.lastName = data.get("lastName", user.lastName)
        return userRepository.save(user)
