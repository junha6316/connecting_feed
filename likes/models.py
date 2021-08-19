from django.db import models
from core.models import TimeStampedModel

class CommentLike(TimeStampedModel):

    comment = models.ForeignKey('comments.Comment', verbose_name="댓글",related_name="comment_likes", on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', verbose_name="좋아요 누른 사람",related_name="comment_likes", on_delete=models.CASCADE)

    class Meta:
        db_table = "comment_likes"


class ReplyLike(TimeStampedModel):
    
    reply = models.ForeignKey('replies.Reply', on_delete=models.CASCADE, related_name="reply_likes")
    user = models.ForeignKey('users.User', verbose_name="좋아요 누른 사람",related_name="reply_likes", on_delete=models.CASCADE)

    class Meta:
        db_table = "reply_likes"


class FeedLike(TimeStampedModel):

    feed = models.ForeignKey('feeds.Feed', on_delete=models.CASCADE, related_name="feed_likes")
    user = models.ForeignKey('users.User', verbose_name="좋아요 누른 사람", related_name="feed_likes", on_delete=models.CASCADE)

    class Meta:
        db_table = "feed_likes"

    
