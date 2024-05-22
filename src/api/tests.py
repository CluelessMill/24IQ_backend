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
from os import path, makedirs, listdir, unlink, rmdir


def init_log() -> None:
    directory = "./src/api/tests_statistic"
    if path.exists(path=directory):
        for filename in listdir(path=directory):
            file_path = path.join(directory, filename)
            try:
                if path.isfile(path=file_path):
                    unlink(path=file_path)
                elif path.isdir(s=file_path):
                    rmdir(path=file_path)
            except Exception as e:
                print(e)
    else:
        makedirs(name=directory)

    basicConfig(filename="./src/api/tests_statistic/logs.log", level=DEBUG)

    ic.configureOutput(prefix="[IC] ", outputFunction=debug)


init_log()


class ServerAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        # init_log()

    def _receive_tokens(self, user: str) -> HttpResponse:
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

    def _set_role_DEBUG(self, new_role: str, nickname: str) -> None:
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
    def test_posts(self) -> None:
        posts_tests(self=self)
