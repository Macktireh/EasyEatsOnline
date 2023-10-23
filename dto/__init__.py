from typing import Optional, TypedDict


class RequestLoginDTO(TypedDict):
    email: str
    password: str


class RequestSignupDTO(RequestLoginDTO):
    firstName: str
    lastName: str
    passwordConfirm: str


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
