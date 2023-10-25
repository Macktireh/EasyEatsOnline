from typing import List

from models.category import Category
from repository.baseRepository import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, model: Category) -> None:
        super().__init__(model)


categoryRepository = CategoryRepository(Category)
