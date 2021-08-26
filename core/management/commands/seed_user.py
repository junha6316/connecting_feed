import random
from datetime import datetime
from django.core.management.base import BaseCommand
from django_seed import Seed


from feeds.models import Feed
from users.models import User


class Command(BaseCommand):

    help = "It seeds the DB with tons of stuff"

    def handle(self, *args, **options):
        #user_seeed
        user_seeder = Seed.seeder()
        user_seeder.add_entity(
            User, 20000, {
              "is_staff": False,
              "is_superuser": False,
              "age": lambda x: random.randint(19, 45)
              }
            )
        user_seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"users are seeded"))