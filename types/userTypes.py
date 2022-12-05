from dataclasses import dataclass


@dataclass
class UserCreateType:
    publicId: str
    email: str
    firstName: str
    lastName: str
    password: str
    passwordConfirm: str
