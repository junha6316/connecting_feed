from inspect import Parameter
from typing import Optional, Tuple

from django.db.models import QuerySet
from django.db.models.fields import IntegerField

from comments.models import Comment
from django.db import models

from core.models import TimeStampedModel
from core.models import (
    image_directory,
    audio_directory,
    gif_directory,
    default_random_name
    )

from users.models import User


class Feed(TimeStampedModel):

    body = models.TextField("내용")
    random_nickname = models.CharField(
        max_length=20,
        default=default_random_name
        )
    audio = models.FileField(upload_to=audio_directory, null=True)
    image = models.ImageField(upload_to=image_directory, null=True)
    gif = models.FileField(upload_to=gif_directory, null=True, default=None)
    user = models.ForeignKey(
        "users.User",
        related_name="feeds",
        on_delete=models.CASCADE
        )
    num_comments = models.IntegerField(default=0)
    num_likes = models.IntegerField(default=0)

    def is_engaged_by(self, user: User) -> Tuple[Optional[bool], Optional[str]]:
        if self._written_by(user):
            return True, self.random_nickname
        if self._has_comment_by(user):
            comment: Comment = self.comments.filter(user=user).first()
            return True, comment.random_nickname
        return None, None

    def _written_by(self, user: User) -> bool:
        return self.user == user

    def _has_comment_by(self, user: User) -> bool:
        comments: QuerySet = self.comments.filter(user=user)
        return comments.exists()

    class Meta:
        db_table = "feeds"
        indexes =[
            models.Index(fields=['created_at']),
            models.Index(fields=['num_likes', 'num_comments', 'created_at'])
        ]
