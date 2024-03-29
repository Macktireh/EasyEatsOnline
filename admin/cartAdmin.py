from typing import List

from flask_admin.helpers import get_form_data

from admin import ModelView
from models.cart import Cart
from repositories.cartRepository import cartRepository


class CartAdmin(ModelView):
    column_list: List[str] = ["publicId", "user.name"]
    # column_editable_list: List[str] = ["userId", "orders"]

    form_excluded_columns = ["publicId"]

    create_modal: bool = True
    edit_modal: bool = True
    can_export: bool = True
    can_view_details: bool = True
    page_size: int = 15

    def on_model_delete(self, model):
        for order in model.orders:
            order.delete()

    def create_model(self, form) -> Cart:
        try:
            form_data = get_form_data()
            try:
                userId = int(form_data.get("user"))
            except ValueError:
                userId = None
            return cartRepository.create(userId)
        except Exception as e:
            raise NotImplementedError from e
