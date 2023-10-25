from typing import List
from slugify import slugify

from flask_admin.helpers import get_form_data
from admin import ModelView

from models.product import Product
from repository.productRepository import productRepository


class ProductAdmin(ModelView):
    column_list: List[str] = [
        "publicId",
        "name",
        "slug",
        "price",
        "category",
        "image",
        "description",
        "available",
        "createdAt",
        "updatedAt",
    ]
    column_hide_backrefs = False
    column_searchable_list: List[str] = ["name", "description"]
    column_filters: List[str] = ["available"]
    column_sortable_list: List[str] = ["createdAt", "updatedAt"]
    column_editable_list: List[str] = [
        "name",
        "price",
        "image",
        "description",
        "available",
    ]
    # form_create_rules: List[str] = [
    #     "name",
    #     "price",
    #     "image",
    #     "description",
    #     "available",
    # ]

    form_excluded_columns = ["publicId", "slug", "createdAt", "updatedAt"]

    create_modal: bool = True
    edit_modal: bool = True
    can_export: bool = True
    can_view_details: bool = True
    page_size: int = 15

    def on_model_change(self, form, model, is_created) -> None:
        if is_created and not model.slug:
            model.slug = slugify(model.name)
        else:
            if model.slug != slugify(model.name):
                model.slug = slugify(model.name)

    def create_model(self, form) -> Product:
        try:
            form_data = get_form_data()
            try:
                categoryId = int(form_data.get("category"))
            except TypeError:
                categoryId = None
            data = {
                "name": form_data.get("name"),
                # "categoryId": categoryId,
                "price": float(form_data.get("price")),
                "image": form_data.get("image"),
                "description": form_data.get("description"),
                "available": True if form_data.get("available") else False,
            }
            return productRepository.create(**data)
        except Exception:
            raise NotImplementedError()
