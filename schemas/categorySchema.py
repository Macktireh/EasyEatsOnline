from flask_restx import Namespace, fields


class CategorySchema:
    api = Namespace("Category", description="category related operations")

    createCategory = api.model(
        "createCategory",
        {
            "name": fields.String(required=True, description="Category Name"),
        },
    )

    category = api.clone(
        "category",
        createCategory,
        {
            "publicId": fields.String(readonly=True, description="category Identifier"),
            "createdAt": fields.DateTime(
                readonly=True, description="Category created at"
            ),
            "updatedAt": fields.DateTime(
                readonly=True, description="Category updated at"
            ),
        },
    )
