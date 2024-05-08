from cgi import test
from django.test import TestCase
from django.urls import reverse
from icecream import ic
from rest_framework.test import APIClient

from .decorators.functions import test_function


class ServerAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def _receive_tokens(self, user: str):
        admin_data = {"email": "admin", "password": "admin"}
        user_data = {"email": "user", "password": "user"}
        data = admin_data if user == "admin" else user_data
        try:
            url = reverse(viewname="sign-up")
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
        data = {"email": "DEFAULT", "password": "DEFAULT"}

        def test_sign_up(self) -> None:
            ic("Sign_up test")
            url = reverse(viewname="sign-up")
            response = self.client.post(path=url, data=data, format="json")
            ic(response.data)
            self.assertEqual(first=response.status_code, second=201)

        def test_sign_in(self) -> None:
            ic("Sign_in test")
            url = reverse(viewname="sign-in")
            response = self.client.post(path=url, data=data, format="json")
            ic(response.data)
            self.assertEqual(first=response.status_code, second=201)

        def test_refresh_token(self) -> None:
            ic("Refresh_token test")
            response = self._receive_tokens(user="user")
            cookie_value = response.cookies["refreshToken"].value
            url = reverse(viewname="refresh-token")
            response = self.client.put(path=url, data=None, format="json")
            response.set_cookie("refreshToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=201)

        test_sign_up(self=self)
        test_sign_in(self=self)
        test_refresh_token(self=self)

    @test_function
    def test_roles(self) -> None:
        def test_role_set(self) -> None:
            ic("Role set test")
            url = reverse(viewname="role-set")

            ic("No permission")
            nickname, cookie_value = self._init_profile(user="user")
            data = {"role": "user", "nickname": nickname}
            response = self.client.put(path=url, data=data, format="json")
            response.set_cookie("accessToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=400)

            ic("With permission")
            nickname, cookie_value = self._init_profile(user="admin")
            ic(nickname)
            self._set_role_DEBUG(new_role="admin", nickname=nickname)
            nickname, new_cookie_value = self._init_profile(user="admin")
            data = {"role": "user", "nickname": nickname}
            response = self.client.put(path=url, data=data, format="json")
            response.set_cookie("accessToken", new_cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=201)

        def test_role_list(self) -> None:
            ic("Roles list test")
            url = reverse(viewname="role-list")

            ic("No permission")
            nickname, cookie_value = self._init_profile(user="user")
            response = self.client.get(path=url, data=None, format="json")
            response.set_cookie("accessToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=400)

            ic("With permission")
            nickname, cookie_value = self._init_profile(user="admin")
            self._set_role_DEBUG(new_role="admin", nickname=nickname)
            response = self.client.get(path=url, data=None, format="json")
            response.set_cookie("accessToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=200)

        def test_is_admin(self) -> None:
            ic("Is admin test")
            url = reverse(viewname="is-admin")

            ic("Admin")
            nickname, cookie_value = self._init_profile(user="admin")
            response = self.client.get(path=url, data=None, format="json")
            response.set_cookie("accessToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=200)
            self.assertEqual(first=response.data["isAdmin"], second=True)

            ic("User")
            nickname, cookie_value = self._init_profile(user="user")
            response = self.client.get(path=url, data=None, format="json")
            response.set_cookie("accessToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=200)
            self.assertEqual(first=response.data["isAdmin"], second=False)

        test_role_set(self=self)
        test_role_list(self=self)
        test_is_admin(self=self)

    @test_function
    def test_posts(self):
        def test_receive_posts(self):
            ic("Receive posts test")
            url = reverse(viewname="posts-list")
            response = self.client.get(path=url, data=None, format="json")
            ic(response.data)
            self.assertEqual(first=response.status_code, second=200)

        def test_create_post(self):
            ic("Create post test")
            url = reverse(viewname="posts-create")

            new_post_data = {
                "title": "Test",
                "text": "Test",
                "category": "Test",
                "logoImg": "Test",
                "mainImg": "Test",
            }
            ic("No permission")
            nickname, cookie_value = self._init_profile(user="user")
            response = self.client.put(path=url, data=new_post_data, format="multipart")
            response.set_cookie("accessToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=400)

            ic("With permission")
            nickname, cookie_value = self._init_profile(user="admin")
            self._set_role_DEBUG(new_role="admin", nickname=nickname)
            with open(file="./api/tests/data/logo.jpg", mode="rb") as logo_file, open(
                file="./api/tests/data/main.jpg", mode="rb"
            ) as main_img_file:
                new_post_data = {
                    "title": "Test",
                    "text": "Test",
                    "category": "Test",
                    "logoImg": ("logo.jpg", logo_file, "image/jpeg"),
                    "mainImg": ("main.jpg", main_img_file, "image/jpeg"),
                }
                response = self.client.put(
                    path=url, data=new_post_data, format="multipart"
                )
                response.set_cookie("accessToken", cookie_value)
                ic(response.data)
                self.assertEqual(first=response.status_code, second=201)

        test_receive_posts(self=self)
        test_create_post(self=self)
