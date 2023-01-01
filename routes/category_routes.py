from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

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
        return CategoryServices.getAllCategories()
    
    @api.response(status.HTTP_201_CREATED, 'Categories successfully added.')
    @api.doc('add_category')
    @api.expect(CategoryDto.ICategory, validate=True)
    @jwt_required()
    def post(self):
        """Add a new Category"""
        return CategoryServices.addCategory(request.json)


@api.route('/<string:publicId>')
class RetrieveUpdateDeleteCategory(Resource):
    
    @api.response(status.HTTP_200_OK, 'category successfully retrieve.')
    @api.doc('retrieve_category')
    @jwt_required()
    def get(self, publicId: str):
        """Retrieve a category"""
        return CategoryServices.getCategoryByPublicId(publicId)
    
    @api.response(status.HTTP_200_OK, 'category successfully updated.')
    @api.doc('update_category')
    @api.expect(CategoryDto.ICategoryUpdate, validate=True)
    @jwt_required()
    def patch(self, publicId: str):
        """Update a category"""
        return CategoryServices.updateCategory(publicId, request.json)
    
    @api.response(status.HTTP_204_NO_CONTENT, 'category successfully deleted.')
    @api.doc('dalete_category')
    @api.expect(CategoryDto.ICategoryUpdate, validate=True)
    @jwt_required()
    def delete(self, publicId: str):
        """Delete a category"""
        return CategoryServices.deleteCategory(publicId)