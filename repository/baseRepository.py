from datetime import datetime
from typing import Any, Dict, List, Tuple, TypeVar
from uuid import uuid4

from app import db


T = TypeVar("T")


class BaseRepository:
    def __init__(self, model: T) -> None:
        self.model = model

    def save(self, _model: T) -> T:
        db.session.add(_model)
        db.session.commit()
        return _model

    def create(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> T:
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
        return self.model.query.all()

    def getById(self, id: int) -> T:
        return self.model.query.get(id)

    def getByPublicId(self, publicId: str) -> T:
        return self.model.query.filter_by(publicId=publicId).first()

    def delete(self, _model: T) -> T:
        db.session.delete(_model)
        db.session.commit()
        return _model
