from django.db import models

from core.models import TimeStampedModel

def image_directory(instance, filename):
    return f"replies/images/{instance.pk}/{filename}"

def audio_directory(instance, filename):
    return f"replies/audio/{instance.pk}/{filename}"

def gif_directory(instance, filename):
    return f"replies/gif/{instance.pk}/{filename}"

class Reply(TimeStampedModel):

    body = models.TextField("내용")
    image = models.ImageField(upload_to=image_directory)
    audio = models.FileField(upload_to=audio_directory, null=True, blank=True)
    gif = models.FileField(upload_to=gif_directory, null=True, blank=True)
    user = models.ForeignKey('users.User', verbose_name="작성자", related_name="replies", on_delete=models.CASCADE)
    comment = models.ForeignKey('comments.Comment', related_name="replies" ,on_delete=models.CASCADE)

    class Meta:
        db_table = "replies"


