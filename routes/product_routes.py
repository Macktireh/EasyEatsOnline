from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.types import ProductType
from schemas.dto import ProductDto
from services.product_service import ProductServices
from utils import status


api = ProductDto.api


@api.route('')
class ListCreateProduct(Resource):
    
    @api.response(status.HTTP_200_OK, 'List of products successfully.')
    @api.doc('list_products')
    @api.marshal_with(ProductDto.IProduct, envelope='data')
    @jwt_required()
    def get(self):
        """List Products"""
        return ProductServices.getAllProducts()
    
    @api.response(status.HTTP_201_CREATED, 'Products successfully added.')
    @api.doc('add_product')
    @api.expect(ProductDto.IProduct, validate=True)
    @jwt_required()
    def post(self):
        """Add a new product"""
        data: ProductType = request.json
        return ProductServices.addProduct(data)


@api.route('/<string:publicId>')
class RetrieveUpdateDeleteProduct(Resource):
    
    @api.response(status.HTTP_200_OK, 'product successfully retrieve.')
    @api.doc('retrieve_product')
    @jwt_required()
    def get(self, publicId: str):
        """Retrieve a product"""
        return ProductServices.getProductByPublicId(publicId)
    
    @api.response(status.HTTP_200_OK, 'product successfully updated.')
    @api.doc('update_product')
    @api.expect(ProductDto.IProductUpdate, validate=True)
    @jwt_required()
    def patch(self, publicId: str):
        """Update a product"""
        data: ProductType = request.json
        return ProductServices.updateProductByPublicId(publicId, data)
    
    @api.response(status.HTTP_204_NO_CONTENT, 'product successfully deleted.')
    @api.doc('dalete_product')
    @jwt_required()
    def delete(self, publicId: str):
        """Delete a product"""
        return ProductServices.deleteProductByPublicId(publicId)