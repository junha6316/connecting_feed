from typing import OrderedDict

from django.db.models.query import Prefetch


from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.fields import SerializerMethodField
from rest_framework.status import HTTP_409_CONFLICT
from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Comment
from users.models import User
from likes.models import CommentLike

from users.serializers import RelatedUserSerializer


class ReplySerializer(ModelSerializer):

    user = RelatedUserSerializer()
    is_my_like = SerializerMethodField()
    is_my_comment = SerializerMethodField()
    to_user = SerializerMethodField()

    def get_is_my_like(self, comment: Comment) -> bool:
        user: User = self.context.get('request').user
        return [
            like for like in comment.likes.all()
            if like.user == user
            ] is not None

    def get_is_my_comment(self, comment: Comment) -> bool:
        user: User = self.context.get('request').user
        comment_user: User = comment.user
        return comment_user.id == user.id

    def get_to_user(self, comment: Comment) -> str:
        return comment.to_user()

    class Meta:
        model = Comment
        exclude = []
        read_only_fields = [
            'created_at',
            'updated_at',
            'random_nickname',
            'num_likes',
            'user',
        ]


class CommentSerializer(ModelSerializer):

    replies = SerializerMethodField()
    is_my_like = SerializerMethodField()
    is_my_comment = SerializerMethodField()
    to_user = SerializerMethodField()

    def get_replies(self, comment: Comment) -> ReturnList:
        if comment.replies.exists():
            query = f'''
                WITH RECURSIVE parents AS (
                    SELECT comments.*, 0 AS relative_depth
                    FROM comments
                    WHERE parent_id = {comment.pk}

                    UNION ALL

                    SELECT comments.*, parents.relative_depth - 1
                    FROM comments, parents
                    WHERE comments.parent_id = parents.id
                )
                SELECT comments.*, users.*, T3.*
                FROM parents as comments
                INNER JOIN feeds
                ON feeds.id = comments.feed_id
                LEFT OUTER JOIN comments as T3
                ON T3.id = comments.parent_id
                INNER JOIN users
                on users.id = comments.user_id
                ORDER BY comments.created_at
                '''
            # 할일: 이부분 Manager로 만들기
            query = f'''
                WITH RECURSIVE parents AS (
                    SELECT comments.*
                    FROM comments
                    WHERE parent_id = {comment.pk}

                    UNION ALL

                    SELECT comments.*
                    FROM comments, parents
                    WHERE comments.parent_id = parents.id
                )
                SELECT comments.*
                FROM parents as comments
                ORDER BY comments.created_at
                '''
            # 문제: join 해서 가져와도 select related가 안먹힘
            replies = Comment.objects.raw(query).prefetch_related(
                Prefetch('likes', CommentLike.objects.select_related('user')),
                Prefetch('parent', Comment.objects.select_related('user')),
                Prefetch('user', User.objects.all())
                )
            serializer = ReplySerializer(replies, many=True)
            serializer.context['request'] = self.context.get('request')
            return serializer.data
        return []

    def get_is_my_like(self, comment: Comment) -> bool:
        user = self.context.get('request').user
        user_likes = [
            like for like in comment.likes.all() if like.user == user
            ] 
        return user_likes is not None

    def get_is_my_comment(self, comment: Comment) -> bool:
        user = self.context.get('request').user
        return comment.user == user

    def get_to_user(self, comment):
        return comment.to_user()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        parent_comment = attrs.get('parent', None)
        feed = attrs.get('feed', None)
        if not parent_comment:
            return attrs
        if parent_comment.feed == feed:
            return attrs
        raise ValidationError(
            detail={"parent": "해당 부모 코멘트가 피드에 포함되어있지 않습니다."},
            code=409
            )
        # 문제 : 409로 에러가 발생하지 않음

    def create(self, validated_data: OrderedDict) -> Comment:
        user: User = self.context.get('request').user

        feed = validated_data.get('feed', None)
        is_engaged, random_nickname = feed.is_engaged_by(user)
        if is_engaged:
            validated_data["random_nickname"] = random_nickname

        now_comment: Comment = Comment.objects.create(
            **validated_data, user=user
            )
        return now_comment

    class Meta:
        model = Comment
        exclude = []
        read_only_fields = [
            'created_at',
            'updated_at',
            'random_nickname',
            'num_likes',
            'user',
            'replies',
        ]
