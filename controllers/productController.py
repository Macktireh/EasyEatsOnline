from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource

from middleware.permissions import admin_required, staff_required
from schemas.productSchema import ProductSchema
from services.productService import ProductService
from utils import status

api = ProductSchema.api


@api.route("")
class ListCreateProduct(Resource):
    @api.response(status.HTTP_200_OK, "List of products successfully.")
    @api.doc("List products")
    @api.marshal_with(ProductSchema.product, envelope="data")
    def get(self):
        """List Products"""
        return ProductService.getAllProducts()

    @api.response(status.HTTP_201_CREATED, "Products successfully added.")
    @api.doc("Add product")
    @api.marshal_with(ProductSchema.product)
    @api.expect(ProductSchema.createProduct, validate=True)
    @jwt_required()
    @staff_required
    def post(self):
        """Add a new product"""
        return ProductService.addProduct(request.json), status.HTTP_201_CREATED


@api.route("/<string:publicId>")
class RetrieveUpdateDeleteProduct(Resource):
    @api.response(status.HTTP_200_OK, "product successfully retrieve.")
    @api.doc("Retrieve product")
    @api.marshal_with(ProductSchema.product)
    def get(self, publicId: str):
        """Retrieve a product"""
        return ProductService.getProduct(publicId)

    @api.response(status.HTTP_200_OK, "product successfully updated.")
    @api.doc("Update product")
    @api.marshal_with(ProductSchema.product)
    @api.expect(ProductSchema.updateProduct, validate=True)
    @jwt_required()
    @staff_required
    def patch(self, publicId: str):
        """Update a product"""
        return ProductService.updateProduct(publicId, request.json)

    @api.response(status.HTTP_204_NO_CONTENT, "product successfully deleted.")
    @api.doc("Delete product")
    @jwt_required()
    @admin_required
    def delete(self, publicId: str):
        """Delete a product"""
        return ProductService.deleteProduct(publicId), status.HTTP_204_NO_CONTENT
