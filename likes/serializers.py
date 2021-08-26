from django.db import IntegrityError
from rest_framework.serializers import ModelSerializer, ValidationError

from likes.models import FeedLike, CommentLike


class LikeSerializer(ModelSerializer):

    def create(self, validated_data):
        user = self.context.get('request').user
        model = self.Meta.model
        try:
            instance = model.objects.create(**validated_data, user=user)
            return instance
        except IntegrityError:
            raise ValidationError({"detail": "이미 해당 글에 좋아요를 눌렀습니다."})


class CommentLikeSerializer(LikeSerializer):

    class Meta:
        model = CommentLike
        exclude = []
        read_only_fields = [
            'user',
        ]


class FeedLikeSerializer(LikeSerializer):

    class Meta:
        model = FeedLike
        exclude = []
        read_only_fields = [
            'user',
        ]
