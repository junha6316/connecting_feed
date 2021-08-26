from django.db import models
from django.dispatch.dispatcher import receiver
from rest_framework.status import HTTP_409_CONFLICT
from rest_framework.serializers import ValidationError


from core.models import TimeStampedModel
from core.models import (
    image_directory,
    audio_directory,
    gif_directory,
    default_random_name
    )


class Comment(TimeStampedModel):

    body = models.TextField('내용')
    random_nickname = models.CharField(
        max_length=20,
        default=default_random_name
        )
    image = models.ImageField(upload_to=image_directory, null=True)
    audio = models.FileField(upload_to=audio_directory, null=True, blank=True)
    gif = models.FileField(upload_to=gif_directory, null=True, blank=True)
    num_likes = models.IntegerField('좋아요 수', default=0)
    # feed와 comment 둘다 있으면 => comment에 달린 댓글
    # comment가 None이면 => feed에 달린 댓글
    parent = models.ForeignKey(
        "self",
        verbose_name="부모 코멘트",
        related_name="replies",
        on_delete=models.CASCADE,
        null=True)
    feed = models.ForeignKey(
        'feeds.Feed',
        verbose_name="피드",
        related_name="comments",
        on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        'users.User',
        verbose_name="작성자",
        related_name="comments",
        on_delete=models.CASCADE
        )

    class Meta:
        db_table = "comments"
        indexes = [
            models.Index(fields=['created_at']),
        ]
    def clean(self):
        if self.parent_comment.feed != self.feed:
            raise ValidationError(
                detail={"parent": "해당 부모 코멘트가 피드에 포함되어있지 않습니다."},
                code=HTTP_409_CONFLICT
                )

    def to_user(self):
        if self.parent:
            return self.parent.random_nickname
        return self.feed.random_nickname

    def __str__(self):
        return f"<Comment Object {self.pk} {self.random_nickname}>"


@receiver(models.signals.pre_save, sender=Comment)
def auto_count_reservation_on_update(sender, instance, **kwargs):
    if instance.id:
        feed = instance.feed
        comment = instance.comment
        if not comment:
            feed.num_comments -= 1
            feed.save()


@receiver(models.signals.post_save, sender=Comment)
def auto_count_reservation_on_create(sender, instance, created, **kwargs):
    feed = instance.feed
    comment = instance.parent
    if not comment:
        feed.num_comments += 1
        feed.save()


