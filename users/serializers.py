
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from django.db.models import Q

from likes.models import CommentLike, FeedLike
from comments.models import Comment

from .models import User


class RelatedUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "sex",
        ]

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = []


class MyActivitySerializer(ModelSerializer):

    num_my_feeds = SerializerMethodField(read_only=True)
    num_my_likes = SerializerMethodField(read_only=True)
    num_my_reply = SerializerMethodField(read_only=True)

    def get_num_my_feeds(self, user: User) -> int:
        return user.feeds.all().count()

    def get_num_my_reply(self, user: User) -> int:
        return user.num_received_comments()

    def get_num_my_likes(self, user: User) -> int:
        return user.num_received_likes()

    class Meta:
        model = User
        fields = ["num_my_feeds", "num_my_likes", "num_my_reply"]
