import json

from rest_framework import status

from todo.tests import TodoApiTestCase


class TaskApiTestCase(TodoApiTestCase):
    fixtures = ("test_users", "test_tags", "test_tasks")

    def test_task_list(self):
        url = f"{self.API_URL}/{self.TASKS_PREFIX}/"

        # Unauthorized user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized user
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

        # Unauthorized user
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized user
        self.api_authentication()
        response = self.client.post(url, data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(content.get("title"), "Go shopping")
        self.assertEqual(content.get("is_completed"), False)
        self.assertEqual(content.get("user", {}).get("username"), self.USER_USERNAME)
        self.assertContains(response, "created_at", status_code=status.HTTP_201_CREATED)
        self.assertContains(response, "updated_at", status_code=status.HTTP_201_CREATED)

        # Double check
        task_id = content.get("id")
        retrieve_url = f"{self.API_URL}/{self.TASKS_PREFIX}/{task_id}/"
        response = self.client.get(retrieve_url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), task_id)
        self.assertEqual(content.get("title"), "Go shopping")
        self.assertEqual(content.get("is_completed"), False)
        self.assertEqual(content.get("user", {}).get("username"), self.USER_USERNAME)
        self.assertEqual(content.get("tags"), "")
        self.assertContains(response, "created_at")
        self.assertContains(response, "updated_at")

    def test_task_retrieve(self):
        url = f"{self.API_URL}/{self.TASKS_PREFIX}/{self.TASK_ID}/"

        # Unauthorized user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized user
        self.api_authentication()
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.TASK_ID)
        self.assertEqual(content.get("title"), "Call the dentist")
        self.assertEqual(content.get("is_completed"), False)
        self.assertEqual(content.get("user", {}).get("username"), self.USER_USERNAME)
        self.assertEqual(content.get("tags"), "health,doctor")
        self.assertEqual(content.get("created_at"), "2020-04-17T01:00:00Z")
        self.assertEqual(content.get("updated_at"), "2020-04-17T01:00:00Z")

    def test_task_update(self):
        url = f"{self.API_URL}/{self.TASKS_PREFIX}/{self.TASK_ID}/"
        data = {
            "is_completed": True
        }

        # Unauthorized user
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Invalid data
        self.api_authentication()
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Get task data and update data
        response = self.client.get(url)
        content = json.loads(response.content)
        title = content.get("title")
        is_completed = not content.get("is_completed")
        data.update({
            "title": title,
            "is_completed": is_completed
        })

        # Authorized user
        response = self.client.put(url, data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.TASK_ID)
        self.assertEqual(content.get("title"), title)
        self.assertEqual(content.get("is_completed"), is_completed)

        # Double check
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.TASK_ID)
        self.assertEqual(content.get("title"), title)
        self.assertEqual(content.get("is_completed"), is_completed)

        # Different user
        different_user_task_url = f"{self.API_URL}/{self.TASKS_PREFIX}/2/"
        response = self.client.put(different_user_task_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_partial_update(self):
        url = f"{self.API_URL}/{self.TASKS_PREFIX}/{self.TASK_ID}/"
        data = {
            "is_completed": True
        }

        # Unauthorized user
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Get task data and update data
        self.api_authentication()
        response = self.client.get(url)
        content = json.loads(response.content)
        is_completed = not content.get("is_completed")
        data.update({
            "is_completed": is_completed
        })

        # Authorized user
        response = self.client.patch(url, data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.TASK_ID)
        self.assertEqual(content.get("title"), "Call the dentist")
        self.assertEqual(content.get("is_completed"), is_completed)

        # Double check
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.TASK_ID)
        self.assertEqual(content.get("title"), "Call the dentist")
        self.assertEqual(content.get("is_completed"), is_completed)

        # Different user
        different_user_task_url = f"{self.API_URL}/{self.TASKS_PREFIX}/2/"
        response = self.client.patch(different_user_task_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_tags(self):
        url = f"{self.API_URL}/{self.TASKS_PREFIX}/{self.TASK_ID}/{self.TAGS_PREFIX}/"
        data = {
            "tags": "health"
        }

        # Unauthorized user
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized user
        self.api_authentication()
        response = self.client.post(url, data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("tags"), "health")

        # Double check
        retrieve_url = f"{self.API_URL}/{self.TASKS_PREFIX}/{self.TASK_ID}/"
        response = self.client.get(retrieve_url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.TASK_ID)
        self.assertEqual(content.get("tags"), "health")

        # Clear tags
        data = {
            "tags": ""
        }
        response = self.client.post(url, data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("tags"), "")

        # Double check
        retrieve_url = f"{self.API_URL}/{self.TASKS_PREFIX}/{self.TASK_ID}/"
        response = self.client.get(retrieve_url)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("id"), self.TASK_ID)
        self.assertEqual(content.get("tags"), "")

        # Different user
        different_user_task_url = f"{self.API_URL}/{self.TASKS_PREFIX}/2/{self.TAGS_PREFIX}/"
        response = self.client.post(different_user_task_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_destroy(self):
        url = f"{self.API_URL}/{self.TASKS_PREFIX}/{self.TASK_ID}/"

        # Unauthorized user
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authorized user
        self.api_authentication()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Double check
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Different user
        different_user_task_url = f"{self.API_URL}/{self.TASKS_PREFIX}/2/"
        response = self.client.delete(different_user_task_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
