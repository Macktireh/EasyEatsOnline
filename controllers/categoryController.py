from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from schemas.categorySchema import CategorySchema
from services.categoryService import CategoryService
from utils import status


api = CategorySchema.api


@api.route("")
class ListCreateCategoryController(Resource):
    @api.response(status.HTTP_200_OK, "List of categories successfully.")
    @api.doc("list_categories")
    @api.marshal_with(CategorySchema.responseCategory, envelope="data")
    @jwt_required()
    def get(self):
        """List Categories"""
        return CategoryService.getAllCategories()

    @api.response(status.HTTP_201_CREATED, "Categories successfully added.")
    @api.doc("add_category")
    @api.marshal_with(CategorySchema.responseCategory)
    @api.expect(CategorySchema.requestCategory, validate=True)
    @jwt_required()
    def post(self):
        """Add a new Category"""
        return CategoryService.addCategory(request.json), status.HTTP_201_CREATED


@api.route("/<string:publicId>")
class RetrieveUpdateDeleteCategoryController(Resource):
    @api.response(status.HTTP_200_OK, "category successfully retrieve.")
    @api.doc("retrieve_category")
    @api.marshal_with(CategorySchema.responseCategory)
    @jwt_required()
    def get(self, publicId: str):
        """Retrieve a category"""
        return CategoryService.getCategory(publicId)

    @api.response(status.HTTP_200_OK, "category successfully updated.")
    @api.doc("update_category")
    @api.marshal_with(CategorySchema.responseCategory)
    @api.expect(CategorySchema.requestCategory, validate=True)
    @jwt_required()
    def patch(self, publicId: str):
        """Update a category"""
        return CategoryService.updateCategory(publicId=publicId, data=request.json)

    @api.response(status.HTTP_204_NO_CONTENT, "category successfully deleted.")
    @api.doc("dalete_category")
    @jwt_required()
    def delete(self, publicId: str):
        """Delete a category"""
        return CategoryService.deleteCategory(publicId), status.HTTP_204_NO_CONTENT
