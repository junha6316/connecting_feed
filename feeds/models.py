from typing import Optional, Tuple

from django.db.models import QuerySet
from comments.models import Comment
from django.db import models

from core.models import TimeStampedModel
from core.models import (
    image_directory,
    audio_directory,
    gif_directory,
    default_random_name,
)

from users.models import User


class Feed(TimeStampedModel):

    body = models.TextField("내용")
    random_nickname = models.CharField(
        "랜덤 닉네임", max_length=20, default=default_random_name
    )
    audio = models.FileField("오디오 파일", upload_to=audio_directory, null=True)
    image = models.ImageField("이미지 파일", upload_to=image_directory, null=True)
    gif = models.FileField("gif 파일", upload_to=gif_directory, null=True, default=None)
    user = models.ForeignKey(
        "users.User", verbose_name="작성자", related_name="feeds", on_delete=models.CASCADE
    )
    num_comments = models.IntegerField("댓글 수", default=0)
    num_likes = models.IntegerField("좋아요 수", default=0)

    def is_engaged_by(self, user: User) -> Tuple[bool, Optional[str]]:
        if self._written_by(user):
            return True, self.random_nickname
        if self._has_comment_by(user):
            comment: Comment = self.comments.filter(user=user).first()
            return True, comment.random_nickname
        return False, None

    def _written_by(self, user: User) -> bool:
        return self.user == user

    def _has_comment_by(self, user: User) -> bool:
        comments: QuerySet = self.comments.filter(user=user)
        return comments.exists()

    class Meta:
        db_table = "feeds"
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["num_likes", "num_comments", "created_at"]),
        ]
