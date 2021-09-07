from users.tokens import AccessToken
from django.test import TestCase
from users.models import User


class UserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        user = User.objects.create(username="test", password="123", age=20)
        user.set_password("123")
        user.save()

        cls.base_url = "/api/v1/users/"

    def test_token_200(self):
        # self.client.login(username="test", password="123")

        token_path = self.base_url + "token/"
        response = self.client.post(
            path=token_path,
            data={
                "username": "test",
                "password": "123",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_issued_refresh_token_is_valid_compared_with_db(self):
        token_path = self.base_url + "token/"
        response = self.client.post(
            path=token_path,
            data={
                "username": "test",
                "password": "123",
            },
        )
        result = response.json()
        refresh_token = result["refresh_token"]
        user = User.objects.get(username="test")
        self.assertEqual(refresh_token, user.refresh_token)

    def test_token_refresh(self):
        token_path = self.base_url + "token/"
        response = self.client.post(
            path=token_path,
            data={
                "username": "test",
                "password": "123",
            },
        )
        result = response.json()
        refresh_token = result["refresh_token"]
        token_refresh_path = token_path + "refresh/"
        response = self.client.post(
            token_refresh_path, {"refresh_token": refresh_token}
        )
        self.assertNotEqual(response.json().get("access_token", None), None)

    def test_token_refresh_without_refresh_token(self):
        token_path = self.base_url + "token/"
        response = self.client.post(
            path=token_path,
            data={
                "username": "test",
                "password": "123",
            },
        )

        token_refresh_path = token_path + "refresh/"
        response = self.client.post(
            token_refresh_path,
        )
        status_code = response.status_code
        error_message = response.json()["detail"]
        self.assertEqual(status_code, 400)
        self.assertEqual(error_message, "토큰이 입력되지 않았습니다.")

    def test_authenticate_fake_token_user_not_existed(self):
        feed_path = "/api/v1/feeds/popular/"
        fake_token = AccessToken(pk=100).encode()
        headers = {"HTTP_AUTHORIZATION": f"Token {fake_token}"}
        response = self.client.get(path=feed_path, **headers)
        self.assertEqual(response.status_code, 403)
