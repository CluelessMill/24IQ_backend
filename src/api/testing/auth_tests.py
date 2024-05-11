from django.urls import reverse
from icecream import ic


def auth_test(self) -> None:
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

        ic("Logout test")
        url = reverse(viewname="logout")
        response = self.client.put(path=url, data=data, format="json")
        response.set_cookie("refreshToken", cookie_value)
        ic(response.data)

    test_sign_up(self=self)
    test_sign_in(self=self)
    test_refresh_token(self=self)
