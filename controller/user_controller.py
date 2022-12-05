from typing import Literal, Dict, Union

from PIL import Image
from io import BytesIO

from flask import request, Response
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from middleware.auth import token_required
from schemas.dto import UserDto
from services.user_service import UserServices
from utils import status


api = UserDto.api

@api.route('/me')
class CurrentUserRoute(Resource):
    @api.doc('get_current_user')
    @api.marshal_list_with(UserDto.IUser, envelope='data')
    @jwt_required()
    def get(self) -> User:
        """Get Current User"""
        identity = get_jwt_identity()
        return UserServices().get_by_publicId(identity["publicId"])

    @api.doc('update_current_user')
    @api.marshal_list_with(UserDto.IUserUpdtae, envelope='data')
    @jwt_required()
    def patch(self) -> Union[tuple[Dict[str, str], Literal[400]], User]:
        """Update Current User"""
        identity = get_jwt_identity()
        return UserServices().update_user_by_publicId(publicId=identity["publicId"], data=request.json)


@api.route('/me/upload')
class UploadImage(Resource):
    @api.doc('upload_image')
    # @api.marshal_list_with(UserDto.IUserUpdtae, envelope='data')
    @jwt_required()
    def patch(self) -> Union[tuple[Dict[str, str], Literal[400]], User]:
        """Update Current User"""
        identity = get_jwt_identity()
        try:
            image = request.files['image']
        except AttributeError:
            return {
                "status": "Fail",
                "message": "image field is required"
            }, status.HTTP_400_BAD_REQUEST
        return UserServices().upload_image(publicId=identity["publicId"], image=image)
    
    @api.marshal_list_with(UserDto.IUser, envelope='data')
    @jwt_required()
    def get(self) -> Union[tuple[Dict[str, str], Literal[400]], User]:
        """Update Current User"""
        identity = get_jwt_identity()
        # try:
        #     image = request.files['image']
        # except AttributeError:
        #     return {
        #         "status": "Fail",
        #         "message": "image field is required"
        #     }, status.HTTP_400_BAD_REQUEST
        
        user = UserServices().get_by_publicId(publicId=identity["publicId"])
        img = Response(user.image.image, mimetype=user.image.nimeType)
        
        # im = Image.open(BytesIO(user.image.image))
        # im.show()
        
        # print()
        # print("img : ", im)
        # print("type img : ", type(im))
        # print()
        
        
        return user


@api.route('')
class CurrentUserRoute(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(UserDto.IUser, envelope='data')
    @jwt_required()
    def get(self):
        """List all registered users"""
        identity = get_jwt_identity()
        return UserServices().get_all_users()
