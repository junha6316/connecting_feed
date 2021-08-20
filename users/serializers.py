import random

from rest_framework import serializers

from faker import Faker
from likes.models import CommentLike, FeedLike, ReplyLike
from rest_framework.fields import SerializerMethodField
from .models import User


class RelatedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "sex",
            "represent_avatar",
            "username",
        ]


class MyActivitySerializer(serializers.ModelSerializer):

    num_my_feeds = serializers.SerializerMethodField(read_only=True)
    num_my_likes = serializers.SerializerMethodField(read_only=True)
    num_my_reply = serializers.SerializerMethodField(read_only=True)

    def get_num_my_feeds(self, obj):
        return obj.feeds.all().count()

    def get_num_my_reply(self, obj):
        return obj.replies.all().count()

    def get_num_my_likes(self, obj):
        feeds = obj.feeds.all()
        feed_likes = FeedLike.objects.filter(feed__id__in=feeds)
        feed_likes_num = feed_likes.count()

        comments = obj.comments.all()
        comment_likes = CommentLike.objects.filter(
            comment__id__in=comments
            )
        comment_likes_num = comment_likes.count()

        replys = obj.replies.all()
        reply_likes = ReplyLike.objects.filter(
            reply__id__in=replys
            )
        reply_likes_num = reply_likes.count()

        return feed_likes_num + comment_likes_num + reply_likes_num

    class Meta:
        model = User
        fields = ["num_my_feeds", "num_my_likes", "num_my_reply"]
