from flask_restx import Namespace, fields

from repositories.categoryRepository import categoryRepository


def productFields(api, required: bool = True):
    return api.model(
        "productFields",
        {
            "name": fields.String(required=required, description="Product Name", example="Pepsi"),
            "price": fields.Float(required=required, description="Product price", example=11.5),
            "description": fields.String(required=False, description="Product description", example="Pepsi Cola 500ml"),
            "image": fields.String(required=False, description="the URL of the product image"),
            "type": fields.String(required=required, description="Product type", example="DRINK"),
        },
    )


class CategoryNameField(fields.Raw):
    def format(self, id) -> str | None:
        if id:
            category = categoryRepository.getById(id)
            return category.name
        return


class ProductSchema:
    api = Namespace("Product", description="product related operations")
    _productFields = productFields(api)

    createProduct = api.clone(
        "createProduct",
        _productFields,
        {
            "categoryPublicId": fields.String(required=False, description="Product Category publicId"),
        },
    )

    updateProduct = api.clone(
        "updateProduct",
        productFields(api, False),
        {
            "categoryPublicId": fields.String(required=False, description="Product Category publicId"),
        },
    )

    product = api.clone(
        "product",
        _productFields,
        {
            "publicId": fields.String(readonly=True, description="product Identifier"),
            "category": CategoryNameField(readonly=True, attribute="categoryId"),
            "available": fields.Boolean(required=False, description="Product available"),
            "createdAt": fields.DateTime(readonly=True, description="Product created at"),
            "updatedAt": fields.DateTime(readonly=True, description="Product updated at"),
            "uri": fields.Url("api.Product_retrieve_update_delete_product", absolute=True),
        },
    )
