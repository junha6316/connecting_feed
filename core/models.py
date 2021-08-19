from django.db import models

class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class BasePostModel(TimeStampedModel):


#     class Meta:
#         abstract = True




