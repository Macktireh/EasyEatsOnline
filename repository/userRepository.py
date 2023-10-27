from typing import Type

from models.user import User
from repository.baseRepository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, model: User) -> None:
        super().__init__(model)

    def createSuperUser(self, *args, **kwargs) -> User:
        """
        Creates a super user with the given arguments.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            User: The created super user.
        """
        self.create(isActive=True, isStaff=True, isAdmin=True, *args, **kwargs)

    def getByEmail(self, email: str) -> User | None:
        """
        Retrieve a user from the database by their email address.

        Parameters:
            email (str): The email address of the user to retrieve.

        Returns:
            User | None: The user with the specified email address, if found.
            None if no user with the email address exists.
        """
        return self.filter(email=email)


userRepository = UserRepository(User)
