from typing import List

from flask_admin.helpers import get_form_data

from admin import ModelView
from models.order import Order
from repositories.orderRepository import orderRepository


class OrderAdmin(ModelView):
    column_list: List[str] = [
        "publicId",
        "user.firstName",
        "user.lastName",
        "product.name",
        "quantity",
        "ordered",
        "createdAt",
        "orderDate",
    ]
    column_filters: List[str] = ["ordered", "quantity"]
    column_sortable_list: List[str] = ["createdAt", "orderDate"]
    column_editable_list: List[str] = ["quantity", "ordered", "orderDate"]

    form_excluded_columns = ["publicId", "ordered", "createdAt"]

    create_modal: bool = True
    edit_modal: bool = True
    can_export: bool = True
    can_view_details: bool = True
    page_size: int = 15

    def create_model(self, form) -> Order:
        try:
            form_data = get_form_data()
            try:
                userId = int(form_data.get("user"))
            except ValueError:
                userId = None
            try:
                productId = int(form_data.get("product"))
            except ValueError:
                productId = None
            data = {
                "userId": userId,
                "productId": productId,
                "quantity": int(form_data.get("quantity")) if form_data.get("quantity") else 1,
            }
            return orderRepository.create(**data)
        except Exception as e:
            raise NotImplementedError from e
