from datetime import datetime
from typing import Any, Dict, List, Tuple, TypeVar
from uuid import uuid4

from werkzeug import exceptions

from config.app import db

Model = TypeVar("Model")


class BaseRepository:
    """A base repository class for handling database operations."""

    def __init__(self, model: Model) -> None:
        self.model = model

    def save(self, _model: Model, update: bool = True) -> Model:
        """
        Saves the given model to the database.

        Parameters:
            _model (Model): The model to be saved.

        Returns:
            Model: The saved model.
        """
        if update:
            _model.updatedAt = datetime.now()
        db.session.commit()
        return _model

    def create(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Model:
        """
        Creates a new instance of the model with the specified arguments and saves it to the database.

        Args:
            *args (Tuple[Any, ...]): The positional arguments to pass to the model constructor.
            **kwargs (Dict[str, Any]): The keyword arguments to pass to the model constructor.

        Returns:
            Model: The newly created model instance.
        """
        _model = self.model(
            *args,
            **kwargs,
            publicId=str(uuid4().hex),
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        )
        db.session.add(_model)
        return self.save(_model, False)

    def filter(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Model | None:
        """
        Find a record in the database based on the provided arguments.

        Args:
            *args (Tuple[Any, ...]): Positional arguments to filter the query.
            **kwargs (Dict[str, Any]): Keyword arguments to filter the query.

        Returns:
            Model | None: The first record that matches the filter, or None if no record is found.
        """
        return self.model.query.filter_by(*args, **kwargs).first()

    def filterAll(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> List[Model]:
        """
        Filter all instances of Model by the given arguments.

        Args:
            *args: Positional arguments passed to the filter method.
            **kwargs: Keyword arguments passed to the filter method.

        Returns:
            List of instances of Model that match the given arguments.
        """
        return self.model.query.filter_by(*args, **kwargs).all()

    def filterAllByExpression(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> List[Model]:
        """
        Filter all instances of Model by the given expression.

        Args:
            *args: Positional arguments passed to the filter method.
            **kwargs: Keyword arguments passed to the filter method.

        Returns:
            List of instances of Model that match the given expression.
        """
        return self.model.query.filter(*args, **kwargs).all()

    def getAll(self) -> List[Model]:
        """
        Returns all the elements in the model.
        :return: List of elements in the model.
        """
        return self.model.query.all()

    def getById(self, id: int) -> Model | None:
        """
        Retrieves an entity from the database by its ID.

        Parameters:
            id (int): The ID of the entity to retrieve.

        Returns:
            Model | None: The retrieved entity if found, or None if not found.
        """
        return self.filter(id=id)

    def getByPublicId(self, publicId: str) -> Model | None:
        """
        Retrieve an instance of type `Model` from the database using the provided public ID.

        Args:
            publicId (str): The public ID of the instance to retrieve.

        Returns:
            Model | None: The instance of type `Model` if found, or `None` if not found.
        """
        return self.filter(publicId=publicId)

    def getOrCreate(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Tuple[Model, bool]:
        """
        Get or create a new instance of the model.

        Args:
            *args (Tuple[Any, ...]): Variable length argument list for filtering the model.
            **kwargs (Dict[str, Any]): Keyword arguments for filtering the model.

        Returns:
            Tuple[Model, bool]: A tuple containing the model instance and a boolean indicating if it was created or not.
        """
        if model := self.model.query.filter_by(*args, **kwargs).first():
            return model, False
        return self.create(*args, **kwargs), True
    
    def getOr404(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Model:
        """
        Get a model instance or raise a 404 error if not found.
    
        Args:
            *args: Positional arguments for filtering the query.
            **kwargs: Keyword arguments for filtering the query.
    
        Returns:
            Model: The retrieved model instance.
    
        Raises:
            NotFound: If the model instance is not found.
        """
        if not (model := self.model.query.filter_by(*args, **kwargs).first()):
            raise exceptions.NotFound(f"{self.model.__name__} not found")
        return model

    def delete(self, _model: Model) -> Model:
        """
        Delete a model object from the database.

        Args:
            _model (Model): The model object to be deleted.

        Returns:
            Model: The deleted model object.
        """
        db.session.delete(_model)
        db.session.commit()
        return _model
