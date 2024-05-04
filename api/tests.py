from django.test import TestCase
from django.urls import reverse
from icecream import ic
from rest_framework.test import APIClient

from .decorators.functions import test_function


class AuthAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def receive_tokens(self) -> str:
        data = {"email": "admin", "password": "admin"}
        url = reverse(viewname="sign-in")
        response = self.client.post(path=url, data=data, format="json")
        self.assertEqual(first=response.status_code, second=201)
        return response

    @test_function
    def test_auth(self) -> None:
        data = {"email": "admin", "password": "admin"}

        def test_sign_up(self) -> None:
            print("Sign_up test")
            url = reverse(viewname="sign-up")
            response = self.client.post(path=url, data=data, format="json")
            self.assertEqual(first=response.status_code, second=201)

        def test_sign_in(self) -> None:
            print("Sign_in test")
            data = {"email": "admin", "password": "admin"}
            url = reverse(viewname="sign-in")
            response = self.client.post(path=url, data=data, format="json")
            self.assertEqual(first=response.status_code, second=201)

        def test_refresh_token(self) -> None:
            print("Refresh_token test")
            response = self.receive_tokens()
            cookie_value = response.cookies["refreshToken"].value
            url = reverse(viewname="refresh-token")
            response = self.client.post(path=url, data=None, format="json")
            response.set_cookie("responseToken", cookie_value)
            self.assertEqual(first=response.status_code, second=201)

        test_sign_up(self=self)
        test_sign_in(self=self)
        test_refresh_token(self=self)

    @test_function
    def test_roles(self) -> None:
        def test_get_roles(self) -> None:
            print("Get_roles test")
            response = self.receive_tokens()
            cookie_value = response.cookies["refreshToken"].value
            url = reverse(viewname="get-roles")
            response = self.client.get(path=url, data=None, format="json")
            response.set_cookie("responseToken", cookie_value)
            self.assertEqual(first=response.status_code, second=200)

        test_get_roles(self=self)
