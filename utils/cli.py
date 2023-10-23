import unittest

from typing import Literal
from unittest import TestResult, TestSuite
from getpass import getpass

from repository.userRepository import userRepository
from utils.validators import validator


def printGreen(text: str) -> None:
    print("\033[92m" + text + "\033[0m")


def printRed(text: str) -> None:
    print("\033[91m" + text + "\033[0m")


def createsuperuserCli() -> None:
    while True:
        email = input("Enter email address: ")
        if email == "":
            printRed("Email is required.")
            continue
        if not validator.validateEmail(email):
            printRed("Email is invalid.")
            continue
        if userRepository.getByEmail(email):
            printRed("A user with this e-mail address already exists.")
            continue

        firstName = input("Enter first name: ")
        lastName = input("Enter last name: ")

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


def testCli() -> Literal[0, 1]:
    tests: TestSuite = unittest.TestLoader().discover("test", pattern="test*.py")
    result: TestResult = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
