from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from django.conf import settings
from django.test import TestCase

from todo.users.models import User


class TodoTestCase(TestCase):
    USER_ID = 1
    USER_USERNAME = "admin"
    USER_PASSWORD = "secret"  # common password for each user.

    @classmethod
    def setUpClass(cls):
        """
        Support YAML format in the fixtures.
        """
        if cls.fixtures:
            new_fixtures = []
            for fixture_name in cls.fixtures:
                new_fixtures.append(f"{settings.FIXTURE_YAML_DIR}/{fixture_name}.yaml")
            cls.fixtures = new_fixtures

        super(TodoTestCase, cls).setUpClass()


class TodoApiTestCase(TodoTestCase):
    API_URL = "/api/v1"
    USERS_PREFIX = "users"

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(username=self.USER_USERNAME)
        self.token, created = Token.objects.get_or_create(user=self.user)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
