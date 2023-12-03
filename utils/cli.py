import json
import unittest
from getpass import getpass
from typing import Literal
from unittest import TestResult, TestSuite

from repository.userRepository import userRepository
from validators.authValidator import AuthValidator


def printGreen(text: str) -> None:
    print("\033[92m" + text + "\033[0m")


def printRed(text: str) -> None:
    print("\033[91m" + text + "\033[0m")


def createSuperUserCli() -> None:
    while True:
        email = input("Enter email address [admin@example.com]: ") or "admin@example.com"
        if email == "":
            printRed("Email is required.")
            continue
        if not AuthValidator.validateEmail(email):
            printRed("Email is invalid.")
            continue
        if userRepository.getByEmail(email):
            printRed("A user with this e-mail address already exists.")
            continue

        firstName = input("Enter first name [John]: ") or "John"
        lastName = input("Enter last name [Doe]: ") or "Doe"

        while True:
            password = getpass("Enter password: ")
            if password == "":
                printRed("Password is required.")
                continue

            confirmPassword = getpass("Enter password again: ")
            if confirmPassword != password:
                printRed("Password and Confirm Password doesn't match.")
                continue

            break

        data = {
            "email": email,
            "firstName": firstName,
            "lastName": lastName,
            "password": password,
        }

        userRepository.createSuperUser(**data)

        printGreen("\nSuper user successfully created.\n")

        break


def runTests(dir: str = "tests", pattern: str = "test*.py", verbosity: int = 2) -> Literal[0, 1]:
    tests: TestSuite = unittest.TestLoader().discover(start_dir=dir, pattern=pattern)
    result: TestResult = unittest.TextTestRunner(verbosity=verbosity).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


def exportPostmanCollection(export: bool = False) -> None:
    from config.app import createApp
    from config.settings import ConfigName
    from urls.api import api, router

    app = createApp(ConfigName.POSTMAN.value)
    app.register_blueprint(router)

    with app.app_context():
        data = api.as_postman(urlvars=False, swagger=True)

    if export:
        with open("postmanCollection.json", "w") as f:
            f.write(json.dumps(data))
            print()
            printGreen("Postman collection exported to 'postmanCollection.json'")
            print()
        return
    print()
    print(json.dumps(data))
    print()
