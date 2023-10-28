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


class RequestCategoryCreateOrUpdateDTO(TypedDict):
    name: str


class RequestProductCreateOrUpdateDTO(RequestCategoryCreateOrUpdateDTO):
    price: float
    type: str
    categoryPublicId: Optional[str]
    description: Optional[str]
    image: Optional[str]


class RequestCreateOrUpdateOrder(TypedDict):
    publicId: int
    quantity: int
