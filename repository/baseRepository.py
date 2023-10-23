from datetime import datetime
from typing import Any, Dict, List, Tuple, TypeVar
from uuid import uuid4

from app import db


T = TypeVar("T")


class BaseRepository:
    def __init__(self, model: T) -> None:
        self.model = model

    def save(self, _model: T) -> T:
        """
        Saves the given model to the database.

        Parameters:
            _model (User): The model to be saved.

        Returns:
            User: The saved model.
        """
        db.session.add(_model)
        db.session.commit()
        return _model

    def create(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> T:
        """
        Creates a new instance of the model with the specified arguments and saves it to the database.

        Args:
            *args (Tuple[Any, ...]): The positional arguments to pass to the model constructor.
            **kwargs (Dict[str, Any]): The keyword arguments to pass to the model constructor.

        Returns:
            User: The newly created model instance.
        """
        _model = self.model(
            *args,
            **kwargs,
            publicId=str(uuid4()),
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        self.save(_model)
        return _model

    def getAll(self) -> List[T]:
        """
        Returns all the elements in the model.
        :return: List of elements in the model.
        """
        return self.model.query.all()

    def getById(self, id: int) -> T | None:
        """
        Retrieves an entity from the database by its ID.

        Parameters:
            id (int): The ID of the entity to retrieve.

        Returns:
            User | None: The retrieved entity if found, or None if not found.
        """
        return self.model.query.get(id)

    def getByPublicId(self, publicId: str) -> T | None:
        """
        Retrieve an instance of type `User` from the database using the provided public ID.

        Args:
            publicId (str): The public ID of the instance to retrieve.

        Returns:
            User | None: The instance of type `User` if found, or `None` if not found.
        """
        return self.model.query.filter_by(publicId=publicId).first()

    def delete(self, _model: T) -> T:
        """
        Delete a model object from the database.

        Args:
            _model (User): The model object to be deleted.

        Returns:
            User: The deleted model object.
        """
        db.session.delete(_model)
        db.session.commit()
        return _model
