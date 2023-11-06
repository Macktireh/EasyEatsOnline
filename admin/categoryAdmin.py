from typing import List

from flask_admin.helpers import get_form_data

from admin import ModelView
from models.category import Category
from repository.categoryRepository import categoryRepository


class CategoryAdmin(ModelView):
    column_editable_list: List[str] = ["name"]
    column_searchable_list: List[str] = ["name"]
    column_sortable_list: List[str] = ["createdAt", "updatedAt"]

    form_excluded_columns: List[str] = ["publicId", "createdAt", "updatedAt"]

    create_modal: bool = True
    edit_modal: bool = True
    can_export: bool = True
    can_view_details: bool = True
    page_size: int = 15

    def create_model(self, form) -> Category:
        try:
            name = get_form_data().get("name")
            return categoryRepository.create(name=name)
        except Exception as e:
            raise NotImplementedError from e
