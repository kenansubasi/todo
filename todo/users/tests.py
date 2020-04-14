import json

from rest_framework import status

from todo.tests import TodoApiTestCase


class UserApiTestCase(TodoApiTestCase):
    fixtures = ("test_user",)

    def test_user_login(self):
        url = f"{self.API_URL}/{self.USERS_PREFIX}/login/"
        data = {
            "username": self.USER_USERNAME,
            "password": self.USER_PASSWORD
        }

        response = self.client.post(url, data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.USER_ID)
        self.assertEqual(content.get("username"), self.USER_USERNAME)
        self.assertEqual(content.get("first_name"), "Admin")
        self.assertEqual(content.get("last_name"), "Todo")
        self.assertContains(response, "auth_token")

    def test_user_logout(self):
        url = f"{self.API_URL}/{self.USERS_PREFIX}/logout/"

        # Unauthorized user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized user
        self.api_authentication()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        url = f"{self.API_URL}/{self.USERS_PREFIX}/{self.USER_USERNAME}/"

        # Unauthorized user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized user
        self.api_authentication()
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.USER_ID)
        self.assertEqual(content.get("username"), self.USER_USERNAME)
        self.assertEqual(content.get("first_name"), "Admin")
        self.assertEqual(content.get("last_name"), "Todo")

        # Different user
        different_user_url = f"{self.API_URL}/{self.USERS_PREFIX}/kenan.subasi/"
        response = self.client.get(different_user_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_update(self):
        url = f"{self.API_URL}/{self.USERS_PREFIX}/{self.USER_USERNAME}/"
        data = {
            "username": "kenan.subasi",
            "email": "admin.todo@todo.com",
            "first_name": "Admin",
            "last_name": "Todo"
        }

        # Unauthorized user
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Existing username
        self.api_authentication()
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Authorized user
        data.update({
            "username": "admin.todo"
        })
        response = self.client.put(url, data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.USER_ID)
        self.assertEqual(content.get("username"), data["username"])
        self.assertEqual(content.get("email"), data["email"])
        self.assertEqual(content.get("first_name"), data["first_name"])
        self.assertEqual(content.get("last_name"), data["last_name"])

        # Different user
        different_user_url = f"{self.API_URL}/{self.USERS_PREFIX}/kenan.subasi/"
        response = self.client.put(different_user_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
