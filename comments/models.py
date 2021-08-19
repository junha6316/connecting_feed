from django.db import models

from core.models import TimeStampedModel


def image_directory(instance, filename):
    return f"comment/images/{instance.pk}/{filename}"

def audio_directory(instance, filename):
    return f"comment/audio/{instance.pk}/{filename}"

def gif_directory(instance, filename):
    return f"comment/gif/{instance.pk}/{filename}"

class Comment(TimeStampedModel):
    
    body = models.TextField('내용')
    image = models.ImageField(upload_to=image_directory, null=True)
    audio = models.FileField(upload_to=audio_directory, null=True, blank=True)
    gif = models.FileField(upload_to=gif_directory, null=True, blank=True)
    feed = models.ForeignKey('feeds.Feed', verbose_name="피드" ,related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', verbose_name="작성자" ,related_name="comments", on_delete=models.CASCADE)

    class Meta:
        db_table = "comments"
        


