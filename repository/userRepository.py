from typing import List

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
        return self.create(*args, **kwargs, isActive=True, isStaff=True, isAdmin=True)

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

    def getAllUsersExceptCurrent(self, publicId: str) -> List[User]:
        """
        Retrieve all users from the database except the current user.

        Parameters:
            publicId (str): The public ID of the current user.

        Returns:
            List[User]: A list of all users except the current user.
        """
        # query: Query = self.model.query.filter(*args, **kwargs)
        # return query.all()
        return self.filterAllByExpression(User.publicId != publicId)


userRepository = UserRepository(User)
