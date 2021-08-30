import random

from django.test import TestCase

from faker import Faker
from django_seed import Seed

from core.models import default_random_name
from users.models import User
from comments.models import Comment
from feeds.models import Feed


class FeedAPITestClass(TestCase):
    @classmethod
    def create_main_user(self):
        user = User.objects.create(username="test", age=20)
        user.set_password("123")
        user.save()

    @classmethod
    def create_users(self):
        user_seeder = Seed.seeder()
        user_seeder.add_entity(
            User,
            10,
            {
                "is_staff": False,
                "is_superuser": False,
                "age": lambda x: random.randint(19, 45),
            },
        )
        user_seeder.execute()

    @classmethod
    def create_feeds(self):
        users = User.objects.all()
        feed_seeder = Seed.seeder()
        for i in range(10):
            faker = Faker()
            Faker.seed(10)
            feed_seeder.add_entity(
                Feed,
                1,
                {
                    "body": lambda x: "\n".join(faker.paragraphs()),
                    "random_nickname": lambda x: default_random_name(),
                    "user": lambda x: random.choice(users),
                    "num_comments": 0,
                    "num_likes": 0,
                },
            )
        feed_seeder.execute()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.create_main_user()
        # cls.create_users()
        # cls.create_feeds()

        cls.base_url = "/api/v1/feeds/"

    def test_get_feed_without_login(self):
        response = self.client.get(path="/api/v1/feeds/")
        self.assertEqual(response.status_code, 403)

    def test_get_feed_latest(self):
        self.client.login(username="test", password="123")
        latest_feed_list_url = self.base_url + "latest/"
        response = self.client.get(path=latest_feed_list_url)
        self.assertEqual(response.status_code, 200)

    def test_get_feed_popular(self):
        self.client.login(username="test", password="123")
        popular_feed_list_url = self.base_url + "popular/"
        response = self.client.get(path=popular_feed_list_url)
        self.assertEqual(response.status_code, 200)

    def test_get_comments_404_if_feed_is_not_existed(self):
        self.client.login(username="test", password="123")
        feed_comment_path = self.base_url + f"{1000000}/comments/"
        response = self.client.get(path=feed_comment_path)
        self.assertEqual(response.status_code, 404)

    def test_get_feed_comment(self):
        user = User.objects.first()
        feed = Feed.objects.create(user=user)

        # Create Comment
        comment1 = Comment.objects.create(
            feed=feed, root=None, user=user
        )  # 피드에 달린 comment
        Comment.objects.create(feed=feed, root=None, user=user)
        Comment.objects.create(
            feed=feed, root=comment1, parent=comment1, user=user
        )  # comment에 달린 comment

        # login
        self.client.login(username="test", password="123")
        feed_comment_path = self.base_url + f"{feed.pk}/comments/"

        response = self.client.get(path=feed_comment_path)
        result_data = response.json()["results"]

        self.assertEqual(len(result_data), 2)
        self.assertEqual(len(result_data[0]["replies"]), 1)

    def test_get_related_comments(self):
        user = User.objects.first()
        feed = Feed.objects.create(user=user)

        self.client.login(feed=feed, user=user)
        # comments_path = self.base_url + f"{feed.pk}/comments"
