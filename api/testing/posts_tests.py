from django.urls import reverse
from icecream import ic


def posts_tests(self) -> None:
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
        with open(file="./api/testing/data/logo.jpg", mode="rb") as logo_file, open(
            file="./api/testing/data/main.jpg", mode="rb"
        ) as main_img_file:
            new_post_data = {
                "title": "Test",
                "text": "Test",
                "category": "Test",
                "logoImg": ("logo.jpg", logo_file, "image/jpeg"),
                "mainImg": ("main.jpg", main_img_file, "image/jpeg"),
            }
            response = self.client.put(path=url, data=new_post_data, format="multipart")
            response.set_cookie("accessToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=201)

    test_receive_posts(self=self)
    test_create_post(self=self)
