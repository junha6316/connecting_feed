import random
from faker import Faker
from datetime import datetime
from django.core.management.base import BaseCommand
from django_seed import Seed

from core.models import default_random_name

from feeds.models import Feed
from users.models import User
from comments.models import Comment


class Command(BaseCommand):

    help = "It seeds the DB with comments"

    def handle(self, *args, **options):
        feeds = Feed.objects.all()
        users = User.objects.all()
        comment_seeder = Seed.seeder()

        for i in range(20):
            faker = Faker()
            Faker.seed(10)
            comment_seeder.add_entity(
                Comment, 2, {
                    'body': lambda x: '\n'.join(faker.paragraphs()),
                    'random_nickname': lambda x: default_random_name(),
                    'num_likes': 0,
                    'parent':None,
                    'feed': lambda x: random.choice(feeds),
                    'user': lambda x: random.choice(users),
                }
            )

        comment_seeder.execute()
        self.stdout.write(self.style.SUCCESS("feed comments are seeded"))
