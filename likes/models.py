from django.dispatch.dispatcher import receiver
from django.db import models
from django.db.models.constraints import UniqueConstraint
from core.models import TimeStampedModel


class CommentLike(TimeStampedModel):

    comment = models.ForeignKey(
        "comments.Comment",
        verbose_name="댓글",
        related_name="likes",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name="좋아요 누른 사람",
        related_name="comment_likes",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "comment_likes"
        constraints = [
            UniqueConstraint(name="comment_like_unique", fields=["user", "comment"])
        ]


class FeedLike(TimeStampedModel):

    feed = models.ForeignKey(
        "feeds.Feed", on_delete=models.CASCADE, related_name="likes"
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name="좋아요 누른 사람",
        related_name="feed_likes",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "feed_likes"
        constraints = [
            UniqueConstraint(name="feed_like_unique", fields=["user", "feed"])
        ]


# CommentLike가 삭제될때 해당 피드 num_likes - 1
@receiver(models.signals.post_delete, sender=CommentLike)
def auto_count_commentLike_on_delete(sender, instance, **kwargs):
    comment = instance.comment
    if comment:
        comment.num_likes -= 1
        comment.save()


# CommentLike가 생성될때 해당 피드 num_likes + 1
@receiver(models.signals.post_save, sender=CommentLike)
def auto_count_commentLike_on_create(sender, instance, created, **kwargs):
    comment = instance.comment
    if comment:
        comment.num_likes += 1
        comment.save()


# Feedlike가 삭제될때 해당 피드 num_likes - 1
@receiver(models.signals.post_delete, sender=FeedLike)
def auto_count_feed_like_on_delete(sender, instance, **kwargs):
    feed = instance.feed
    if feed:
        feed.num_likes -= 1
        feed.save()


# Feedlike가 생성될때 해당 피드 num_likes + 1
@receiver(models.signals.post_save, sender=FeedLike)
def auto_count_feed_like_on_create(sender, instance, created, **kwargs):
    feed = instance.feed
    if feed:
        feed.num_likes += 1
        feed.save()
