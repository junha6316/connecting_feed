from django.db import models
from django.dispatch.dispatcher import receiver
from rest_framework.serializers import ValidationError


from core.models import TimeStampedModel
from core.models import (
    image_directory,
    audio_directory,
    gif_directory,
    default_random_name,
)


class Comment(TimeStampedModel):

    body = models.TextField("내용")
    random_nickname = models.CharField(
        "랜덤 닉네임", max_length=20, default=default_random_name
    )
    image = models.ImageField(
        "이미지 파일", upload_to=image_directory, null=True, blank=True
    )
    audio = models.FileField("오디오 파일", upload_to=audio_directory, null=True, blank=True)
    gif = models.FileField("gif 파일", upload_to=gif_directory, null=True, blank=True)
    num_likes = models.IntegerField("좋아요 수", default=0)
    # feed와 comment 둘다 있으면 => comment에 달린 댓글
    # comment가 None이면 => feed에 달린 댓글
    root = models.ForeignKey(
        "self",
        related_name="replies",
        verbose_name="루트 코멘트",
        on_delete=models.CASCADE,
        null=True,
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="부모 코멘트",
        related_name="child_comment",
        on_delete=models.CASCADE,
        null=True,
    )
    feed = models.ForeignKey(
        "feeds.Feed",
        verbose_name="피드",
        related_name="comments",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name="작성자",
        related_name="comments",
        on_delete=models.CASCADE,
    )

    def clean(self):
        feed = self.cleaned_data["feed"]
        parent = self.cleaned_data["parent"]
        root = self.cleaned_data["root"]

        if not root:  # 피드에 달린 코멘트
            return self.cleaned_data
        elif root.feed == feed:
            return self.cleaned_data
        elif parent.feed == feed:
            return self.cleaned_data

        raise ValidationError(
            detail={"parent": "해당 부모 코멘트가 피드에 포함되어있지 않습니다."}, code=409
        )

    def save(self, *args, **kwargs):
        feed, user = self.feed, self.user
        is_engaged, pre_random_name = feed.is_engaged_by(user)
        if is_engaged:
            self.random_nickname = pre_random_name
        super().save(*args, **kwargs)

    def to_user(self):
        if self.parent:
            return self.parent.random_nickname
        return self.feed.random_nickname

    def __str__(self):
        return f"<Comment Object {self.pk} {self.random_nickname}>"

    class Meta:
        db_table = "comments"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["feed", "parent"]),
        ]


@receiver(models.signals.post_delete, sender=Comment)
def auto_count_reservation_on_update(sender, instance, **kwargs):
    if instance.id:
        feed = instance.feed
        parent_comment = instance.parent
        if not parent_comment:
            feed.num_comments -= 1
            feed.save()


@receiver(models.signals.post_save, sender=Comment)
def auto_count_reservation_on_create(sender, instance, created, **kwargs):
    feed = instance.feed
    parent_comment = instance.parent
    if not parent_comment:
        feed.num_comments += 1
        feed.save()
