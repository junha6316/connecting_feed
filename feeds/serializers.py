from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField

from users.serializers import RelatedUserSerializer
from core.models import default_random_name

from .models import Feed


class BaseFeedSerializer(ModelSerializer):

    user = RelatedUserSerializer(read_only=True)
    is_like = SerializerMethodField(read_only=True)

    def get_is_like(self, feed):
        user = self.context.get("request").user
        # cache => feed.likes.filter(user=user)
        # 해당 피드의 좋아요를 눌렀는지 확인
        # 아래처럼 적어줘야 추가 쿼리가 안나간다.
        return len([like for like in feed.likes.all() if like.user == user])

    class Meta:
        model = Feed
        exclude = ["updated_at"]
        read_only_fields = ["num_likes", "num_comments", "random_nickname"]


class FeedListSerializer(BaseFeedSerializer):
    def create(self, validated_data):
        user = self.context.get("request").user
        random_nickname = default_random_name()
        feed = Feed.objects.create(
            **validated_data, random_nickname=random_nickname, user=user
        )
        return feed
