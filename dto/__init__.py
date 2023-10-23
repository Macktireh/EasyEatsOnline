from typing import Optional, TypedDict


class RequestUserUpdateDTO(TypedDict):
    firstName: str
    lastName: str


class RequestLoginDTO(TypedDict):
    email: str
    password: str


class RequestSignupDTO(RequestUserUpdateDTO, RequestLoginDTO):
    passwordConfirm: str


class RequestActivateDTO(TypedDict):
    token: str


class TokenPayload(TypedDict):
    publicId: str
    isActive: bool


class ProductType(TypedDict):
    name: str
    categoryId: Optional[int]
    price: float
    description: Optional[str]
    image: Optional[str]
    available: bool


class CategoryType(TypedDict):
    name: str
