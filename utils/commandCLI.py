from typing import Dict, Literal, Union
import unittest
from unittest import TestResult, TestSuite

from getpass import getpass
from services.user_service import UserServices
from utils import validators


def createsuperuser_cli(cls: UserServices) -> None:
    emailValid: bool = False
    passwordValid: bool = False
    confirmPassword: Union[str, None] = None
    while not emailValid:
        email: str = input("Email : ")
        if email != "":
            if validators.validate_email(email):
                
                if not cls.get_by_email(email):
                    emailValid = True
                    firstName: str = input("First Name : ")
                    lastName: str = input("Last Name : ")
                    while not passwordValid:
                        password: str = getpass("Password : ")
                        if password != "":
                            passwordValid = True
                            while confirmPassword is None:
                                _confirmPassword: str = getpass("Confirm Password : ")
                                if _confirmPassword == password:
                                    confirmPassword = _confirmPassword
                                else:
                                    print("Password and Confirm Password doesn't match.")
                        else:
                            print("Password is required.")
                            
                    data: Dict[str, str] = {"email": email, "firstName": firstName, "lastName": lastName, "password": password}
                    cls.create_superuser(data)
                    print()
                    print("Super user successfully created.")
                    print()
                else:
                    print("A user with this e-mail address already exists.")
            else:
                print("Email is invalid.")
        else:
            print("Email is required.")


def test_cli() -> Literal[0, 1]:
    tests: TestSuite = unittest.TestLoader().discover('test', pattern='test*.py')
    result: TestResult = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1