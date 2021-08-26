from django.db import models


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def image_directory(instance, filename):
    model_name = instance._meta.model_name
    return f"media/{model_name}/images/{filename}"


def audio_directory(instance, filename):
    model_name = instance._meta.model_name
    return f"media/{model_name}/audio/{filename}"


def gif_directory(instance, filename):
    model_name = instance._meta.model_name
    return f"media/{model_name}/gif/{filename}"


