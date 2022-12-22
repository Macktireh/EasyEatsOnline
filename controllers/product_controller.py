from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from schemas.dto import ProductDto
from services.product_service import ProductServices
from utils import status


api = ProductDto.api


@api.route('')
class ListOrCreateProduct(Resource):
    
    @api.doc('list_products')
    @api.marshal_list_with(ProductDto.IProduct, envelope='data')
    @jwt_required()
    def get(self):
        """List Products"""
        return ProductServices.get_all_products()

    @api.doc('create_all_products')
    @api.marshal_list_with(ProductDto.IProduct, envelope='data')
    @jwt_required()
    def post(self):
        """Update Current User"""
        data: dict = request.json
        return data, status.HTTP_200_OK


@api.route('/<string:publicId>')
class UpdateOrDeleteProduct(Resource):
    
    @api.doc('list_products')
    @api.marshal_list_with(ProductDto.IProduct, envelope='data')
    @jwt_required()
    def patch(self, publicId: str):
        """List Products"""
        return ProductServices.get_all_products()

    @api.doc('create_all_products')
    @api.marshal_list_with(ProductDto.IProduct, envelope='data')
    @jwt_required()
    def delete(self, publicId: str):
        """Update Current User"""
        data: dict = request.json
        return data, status.HTTP_200_OK