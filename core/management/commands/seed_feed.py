import random
from faker import Faker
from django.core.management.base import BaseCommand
from django_seed import Seed

from core.models import default_random_name
from feeds.models import Feed
from users.models import User


class Command(BaseCommand):

    help = "It seeds the DB with tons of stuff"

    def handle(self, *args, **options):
        users = User.objects.all()
        feed_seeder = Seed.seeder()
        for i in range(10000):
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
        self.stdout.write(self.style.SUCCESS("feeds are seeded"))
