import unittest

from flask import Flask, url_for
from flask_testing import TestCase

from app import createApp, db
from controllers import apiRoute
from repository.userRepository import userRepository
from tests.fixture import Fixture
from utils import status


class CategoryControllerTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        app.register_blueprint(apiRoute)
        return app

    def setUp(self) -> None:
        db.create_all()
        self.category = Fixture.createCategories(1)[0]
        self.userActive, self.userAdmin, self.userStaff = Fixture.createUsers(3)

        self.userActive.isActive = True
        userRepository.save(self.userActive)

        self.userStaff.isActive = True
        self.userStaff.isStaff = True
        userRepository.save(self.userStaff)

        res = self.client.post(
            url_for("api.Auth_login_controller"), json={"email": self.userActive.email, "password": "password"}
        )
        self.headersActive = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {res.json["tokens"]["access"]}',
        }
        res = self.client.post(
            url_for("api.Auth_login_controller"), json={"email": self.userAdmin.email, "password": "password"}
        )
        self.headersAdmin = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {res.json["tokens"]["access"]}',
        }

        res = self.client.post(
            url_for("api.Auth_login_controller"), json={"email": self.userStaff.email, "password": "password"}
        )
        self.headersStaff = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {res.json["tokens"]["access"]}',
        }

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_controller_category_list_categories(self) -> None:
        res = self.client.get(url_for("api.Category_list_create_category_controller"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_controller_category_create_category_ok(self) -> None:
        response = self.client.post(
            url_for("api.Category_list_create_category_controller"), json={"name": "test"}, headers=self.headersAdmin
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_controller_category_create_category_fail(self) -> None:
        response = self.client.post(
            url_for("api.Category_list_create_category_controller"), json={"name": ""}, headers=self.headersAdmin
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test user is not authenticated
        response = self.client.post(
            url_for("api.Category_list_create_category_controller"),
            json={"name": "test2"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test user is not staff
        response = self.client.post(
            url_for("api.Category_list_create_category_controller"), json={"name": ""}, headers=self.headersActive
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_controller_category_retrieve_category_ok(self) -> None:
        response = self.client.get(
            url_for("api.Category_retrieve_update_delete_category_controller", publicId=self.category.publicId),
            headers=self.headersAdmin,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_controller_category_retrieve_category_fail(self) -> None:
        response = self.client.get(
            url_for("api.Category_retrieve_update_delete_category_controller", publicId="wrongpublicId"),
            headers=self.headersAdmin,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_controller_category_update_category_ok(self) -> None:
        response = self.client.patch(
            url_for("api.Category_retrieve_update_delete_category_controller", publicId=self.category.publicId),
            json={"name": "test"},
            headers=self.headersAdmin,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_controller_category_update_category_fail(self) -> None:
        response = self.client.patch(
            url_for("api.Category_retrieve_update_delete_category_controller", publicId="wrongpublicId"),
            json={"name": "test"},
            headers=self.headersAdmin,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # test user is not authenticated
        response = self.client.patch(
            url_for("api.Category_retrieve_update_delete_category_controller", publicId=self.category.publicId),
            json={"name": "test2"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test user is not staff
        response = self.client.patch(
            url_for("api.Category_retrieve_update_delete_category_controller", publicId=self.category.publicId),
            json={"name": "test2"},
            headers=self.headersActive,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_controller_category_delete_category_ok(self) -> None:
        response = self.client.delete(
            url_for("api.Category_retrieve_update_delete_category_controller", publicId=self.category.publicId),
            headers=self.headersAdmin,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_controller_category_delete_category_fail(self) -> None:
        response = self.client.delete(
            url_for("api.Category_retrieve_update_delete_category_controller", publicId="wrongpublicId"),
            headers=self.headersAdmin,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # test user is not authenticated
        response = self.client.delete(
            url_for("api.Category_retrieve_update_delete_category_controller", publicId=self.category.publicId),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test user is not admin
        response = self.client.delete(
            url_for("api.Category_retrieve_update_delete_category_controller", publicId=self.category.publicId),
            headers=self.headersActive,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test user is not admin
        response = self.client.delete(
            url_for("api.Category_retrieve_update_delete_category_controller", publicId=self.category.publicId),
            headers=self.headersStaff,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


if __name__ == "__main__":
    unittest.main()
