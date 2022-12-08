import unittest

from getpass import getpass
from utils import validators


def createsuperuser_cli(UserServices):
    emailValid = False
    passwordValid = False
    confirmPassword = None
    while not emailValid:
        email = input("Email : ")
        if email != "":
            if validators.validate_email(email):
                
                if not UserServices.get_by_email(email):
                    emailValid = True
                    firstName = input("First Name : ")
                    lastName = input("Last Name : ")
                    while not passwordValid:
                        password = getpass("Password : ")
                        if password != "":
                            passwordValid = True
                            while confirmPassword is None:
                                pc = getpass("Confirm Password : ")
                                if pc == password:
                                    confirmPassword = pc
                                else:
                                    print("Password and Confirm Password doesn't match.")
                        else:
                            print("Password is required.")
                            
                    data = {"email": email, "firstName": firstName, "lastName": lastName, "password": password}
                    UserServices.create_superuser(data)
                    print()
                    print("Super user successfully created.")
                    print()
                else:
                    print("A user with this e-mail address already exists.")
            else:
                print("Email is invalid.")
        else:
            print("Email is required.")


def test_cli():
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1