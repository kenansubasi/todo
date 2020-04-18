import json

from rest_framework import status

from todo.tests import TodoApiTestCase


class TaskApiTestCase(TodoApiTestCase):
    fixtures = ("test_users", "test_tasks")

    def test_task_list(self):
        url = f"{self.API_URL}/{self.TASKS_PREFIX}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.api_authentication()
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 4)

    def test_task_create(self):
        url = f"{self.API_URL}/{self.TASKS_PREFIX}/"
        data = {
            "title": "Go shopping"
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.api_authentication()
        response = self.client.post(url, data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(content.get("title"), "Go shopping")
        self.assertEqual(content.get("is_completed"), False)
        self.assertEqual(content.get("user", {}).get("username"), self.USER_USERNAME)
        self.assertContains(response, "created_at", status_code=status.HTTP_201_CREATED)
        self.assertContains(response, "updated_at", status_code=status.HTTP_201_CREATED)
