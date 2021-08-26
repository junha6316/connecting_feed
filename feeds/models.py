import random

from faker import Faker
from django.db import models

from core.models import TimeStampedModel, image_directory, audio_directory


def default_random_name():
    faker = Faker(['ko-KR'])
    seed_value = random.randint(1, 20000)
    Faker.seed(seed_value)
    return faker.bs()


class Feed(TimeStampedModel):

    body = models.TextField("내용")
    random_nickname = models.CharField(
        max_length=20,
        default=default_random_name
        )
    audio = models.FileField(upload_to=audio_directory, null=True)
    image = models.ImageField(upload_to=image_directory, null=True)
    user = models.ForeignKey(
        "users.User",
        related_name="feeds",
        on_delete=models.CASCADE
        )

    class Meta:
        ordering = ["-created_at"]
        db_table = "feeds"
