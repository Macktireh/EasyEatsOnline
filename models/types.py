from typing import Optional, TypedDict


class UserType(TypedDict): 
    email: str
    firstName: str
    lastName: str
    password: str
    passwordConfirm: str


class TokenIdentityType(TypedDict): 
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