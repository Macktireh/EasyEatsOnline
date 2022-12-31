from typing import Any
from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.types import CategoryType
from schemas.dto import CategoryDto
from services.category_service import CategoryServices
from utils import status


api = CategoryDto.api


@api.route('')
class ListCreateCategory(Resource):
    
    @api.response(status.HTTP_200_OK, 'List of categories successfully.')
    @api.doc('list_categories')
    @api.marshal_with(CategoryDto.ICategory, envelope='data')
    @jwt_required()
    def get(self):
        """List Categories"""
        try:
            return CategoryServices.getAllCategories()
        except Exception as e:
            return {
                    "message": "Something went wrong!",
                    "error": str(e),
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @api.response(status.HTTP_201_CREATED, 'Categories successfully added.')
    @api.doc('add_category')
    @api.expect(CategoryDto.ICategory, validate=True)
    @jwt_required()
    def post(self):
        """Add a new Category"""
        try:
            data: CategoryType = request.json
            return CategoryServices.addCategory(data)
        except Exception as e:
            return {
                    "message": "Something went wrong!",
                    "error": str(e),
            }, status.HTTP_500_INTERNAL_SERVER_ERROR


@api.route('/<string:publicId>')
class RetrieveUpdateDeleteCategory(Resource):
    
    @api.response(status.HTTP_200_OK, 'category successfully retrieve.')
    @api.doc('retrieve_category')
    @jwt_required()
    def get(self, publicId: str):
        """Retrieve a category"""
        try:
            return CategoryServices.getCategoryByPublicId(publicId)
        except Exception as e:
            return {
                    "message": "Something went wrong!",
                    "error": str(e),
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @api.response(status.HTTP_200_OK, 'category successfully updated.')
    @api.doc('update_category')
    @api.expect(CategoryDto.ICategoryUpdate, validate=True)
    @jwt_required()
    def patch(self, publicId: str):
        """Update a category"""
        try:
            data: CategoryType = request.json
            return CategoryServices.updateCategory(publicId, data)
        except Exception as e:
            return {
                    "message": "Something went wrong!",
                    "error": str(e),
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @api.response(status.HTTP_204_NO_CONTENT, 'category successfully deleted.')
    @api.doc('dalete_category')
    @api.expect(CategoryDto.ICategoryUpdate, validate=True)
    @jwt_required()
    def delete(self, publicId: str):
        """Delete a category"""
        try:
            return CategoryServices.deleteCategory(publicId)
        except Exception as e:
            return {
                    "message": "Something went wrong!",
                    "error": str(e),
            }, status.HTTP_500_INTERNAL_SERVER_ERROR