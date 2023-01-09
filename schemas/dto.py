from flask_restplus import Namespace, fields

from models.category import Category


class AuthDto:
    
    api = Namespace('Auth', description='user auth')
    
    ISignup = api.model('signup', {
        'email': fields.String(required=True, description='user email address'),
        'firstName': fields.String(required=True, description='user firstname'),
        'lastName': fields.String(required=True, description='user lastname'),
        'publicId': fields.String(description='user Identifier'),
        'password': fields.String(required=True, description='user password'),
        'passwordConfirm': fields.String(required=True, description='user password confirm'),
    })
    
    ILogin = api.model('login', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })
    
    IToken = api.model('token', {
        'token': fields.String(required=True, description='token'),
    })


class UserDto:
    
    api = Namespace('User', description='user related operations')
    
    IUser = api.model('users', {
        'publicId': fields.String(description='user Identifier'),
        'email': fields.String(required=True, description='user email address'),
        'firstName': fields.String(required=True, description='user firstname'),
        'lastName': fields.String(required=True, description='user lastname'),
    })
    
    IUserUpdate = api.model('UserUpdate', {
        'firstName': fields.String(required=False, description='user firstname'),
        'lastName': fields.String(required=False, description='user lastname'),
    })


class CategoryNameField(fields.Raw):
    
    def format(self, id):
        if id:
            category = Category.getById(id)
            return category.name
        return

class ProductDto:
    
    api = Namespace('Product', description='product related operations')
    
    IProduct = api.model('product', {
        'publicId': fields.String(readonly=True, description='product Identifier'),
        'name': fields.String(required=True, description='Product Name'),
        'categoryPublicId': fields.String(required=False, description='Product Category publicId'),
        'category': CategoryNameField(readonly=True, attribute='categoryId'),
        'price': fields.Float(required=True, description='Product price'),
        'image': fields.String(required=False, description='the URL of the product image'),
        'description': fields.String(required=False, description='Product description'),
        'available': fields.Boolean(required=False, description='Product available'),
        'createdAt': fields.DateTime(readonly=True, description='Product created at'),
        'updatedAt': fields.DateTime(readonly=True, description='Product updated at'),
    }, mask='{publicId, name, category, price, image, description, available, createdAt, updatedAt}')
    
    IProductUpdate = api.model('productUpdate', {
        'publicId': fields.String(readonly=True, description='product Identifier'),
        'name': fields.String(required=False, description='Product Name'),
        'categoryPublicId': fields.String(required=False, description='Product Category publicId'),
        'category': CategoryNameField(readonly=True, attribute='categoryId'),
        'price': fields.Float(required=False, description='Product price'),
        'image': fields.String(required=False, description='the URL of the product image'),
        'description': fields.String(required=False, description='Product description'),
        'available': fields.Boolean(required=False, description='Product available'),
        'createdAt': fields.DateTime(readonly=True, description='Product created at'),
        'updatedAt': fields.DateTime(readonly=True, description='Product updated at'),
    }, mask='{publicId, name, category, price, image, description, available, createdAt, updatedAt}')


class CategoryDto:
    
    api = Namespace('Category', description='category related operations')
    
    ICategory = api.model('category', {
        'publicId': fields.String(readonly=True, description='product Identifier'),
        'name': fields.String(required=True, description='Product Name'),
        'createdAt': fields.DateTime(readonly=True, description='Product created at'),
        'updatedAt': fields.DateTime(readonly=True, description='Product updated at'),
    })
    
    ICategoryUpdate = api.model('categoryUpdate', {
        'publicId': fields.String(readonly=True, description='product Identifier'),
        'name': fields.String(required=False, description='Product Name'),
        'createdAt': fields.DateTime(readonly=True, description='Product created at'),
        'updatedAt': fields.DateTime(readonly=True, description='Product updated at'),
    })


class CartDto:
    
    api = Namespace('Cart', description='Cart related operations')