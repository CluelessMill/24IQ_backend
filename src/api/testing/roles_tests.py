from django.urls import reverse
from icecream import ic


def roles_test(self) -> None:
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
