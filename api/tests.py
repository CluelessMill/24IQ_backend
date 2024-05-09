from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from icecream import ic
from rest_framework.test import APIClient

from .decorators.functions import test_function
from .testing.auth_tests import auth_test
from .testing.roles_tests import roles_test
from .testing.posts_tests import posts_tests
from logging import basicConfig, debug, DEBUG

basicConfig(filename="./api/tests_statistic/logs.log", level=DEBUG)
ic.configureOutput(prefix="[IC] ", outputFunction=debug)


class ServerAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def _receive_tokens(self, user: str):
        admin_data = {"email": "admin", "password": "admin"}
        user_data = {"email": "user", "password": "user"}
        data = admin_data if user == "admin" else user_data
        try:
            url = reverse(viewname="sign-up")
            HttpResponse
            response = self.client.post(path=url, data=data, format="json")
            self.assertEqual(first=response.status_code, second=201)
        except Exception as e:
            pass
        url = reverse(viewname="sign-in")
        response = self.client.post(path=url, data=data, format="json")
        self.assertEqual(first=response.status_code, second=201)
        return response

    def _init_profile(self, user):
        token_request = self._receive_tokens(user=user)
        nickname = token_request.data["user"]["nickname"]
        cookie_value = token_request.cookies["accessToken"].value
        return nickname, cookie_value

    def _set_role_DEBUG(self, new_role: str, nickname: str):
        url = reverse(viewname="role-set-deb")
        data = {"role": new_role, "nickname": nickname}
        response = self.client.put(path=url, data=data, format="json")
        self.assertEqual(first=response.status_code, second=201)

    @test_function
    def test_auth(self) -> None:
        auth_test(self=self)

    @test_function
    def test_roles(self) -> None:
        roles_test(self=self)

    @test_function
    def test_posts(self):
        posts_tests(self=self)
