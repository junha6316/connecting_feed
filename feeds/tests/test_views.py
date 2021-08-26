from datetime import time
import random

from rest_framework.test import APIRequestFactory, APIClient
from django.test import TestCase
from django.utils import timezone

from faker import Faker, factory
from django_seed import Seed
from users.models import User
from core.models import default_random_name
from feeds.models import Feed

class FeedAPITestClass(TestCase):

    @classmethod
    def create_main_user(self):
        user = User.objects.create(username="test", age=20)
        user.set_password('123')
        user.save()

    @classmethod
    def create_users(self):
        user_seeder = Seed.seeder()
        user_seeder.add_entity(
            User, 10, {
              "is_staff": False,
              "is_superuser": False,
              "age": lambda x: random.randint(19, 45)
              }
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
                Feed, 1, {
                    'created_at': timezone.now(),
                    'body': lambda x: '\n'.join(faker.paragraphs()),
                    'random_nickname': lambda x: default_random_name(),
                    'user': lambda x: random.choice(users),
                    'num_comments': 0,
                    'num_likes': 0,
                }
                )
        feed_seeder.execute()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.create_main_user()
        cls.create_users()
        cls.create_feeds()

    def test_get_feed_without_login(self):
        response = self.client.get(
            path="/api/v1/feeds/"
        )
        self.assertEqual(response.status_code, 403)

    def test_get_feed_with_login(self):
        self.client.login(username="test", password="123")
        response = self.client.get(
            path=f"/api/v1/feeds/"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_feed(self):
        self.client.login(username="test", password="123")
        response = self.client.get(
            path=f"/api/v1/feeds/"
        )
        print(response.json())

        self.assertEqual(response.status_code, 200)

    def test_post_feed(self):
        self.client.login(username="test", password="123")
        response = self.client.post(
            path="/api/v1/feeds/",
            content_type="application/json",
            data={
                "body": "test",
            }
        )





