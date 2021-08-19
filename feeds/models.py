from django.db import models

from core.models import TimeStampedModel

def image_directory(instance, filename):
    return f"feed/images/{instance.pk}/{filename}"

def audio_directory(instance, filename):
    return f"feed/audio/{instance.pk}/{filename}"

class Feed(TimeStampedModel):

    body = models.TextField()
    audio = models.FileField(upload_to=audio_directory)
    image = models.ImageField(upload_to=image_directory)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        db_table="feeds"
