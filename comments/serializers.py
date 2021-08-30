from typing import OrderedDict

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from .models import Comment
from users.models import User

from users.serializers import RelatedUserSerializer


class BaseCommentSerializer(ModelSerializer):

    user = RelatedUserSerializer(read_only=True)
    is_my_like = SerializerMethodField()
    is_my_comment = SerializerMethodField()
    to_user = SerializerMethodField()

    def get_is_my_like(self, comment: Comment) -> bool:
        user: User = self.context.get("request").user
        user_likes = [like for like in comment.likes.all() if like.user == user]
        return len(user_likes) > 0

    def get_is_my_comment(self, comment: Comment) -> bool:
        user: User = self.context.get("request").user
        comment_user: User = comment.user
        return comment_user.id == user.id

    def get_to_user(self, comment: Comment) -> str:
        return comment.to_user()

    class Meta:
        model = Comment
        exclude = []
        read_only_fields = [
            "created_at",
            "updated_at",
            "random_nickname",
            "num_likes",
            "user",
        ]


class ReplySerializer(BaseCommentSerializer):

    pass


class CommentSerializer(BaseCommentSerializer):

    replies = ReplySerializer(many=True, read_only=True)

    def create(self, validated_data: OrderedDict) -> Comment:
        user: User = self.context.get("request").user
        now_comment: Comment = Comment.objects.create(**validated_data, user=user)
        return now_comment
