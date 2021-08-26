from functools import cache
import random
from datetime import timedelta
from faker import Faker

from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.serializers import RelatedUserSerializer

from likes.models import FeedLike
from core.models import default_random_name
from .models import Feed


class BaseFeedSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer(read_only=True)
    is_like = SerializerMethodField(read_only=True)
    # created_at = serializers.SerializerMethodField()
    # num_feed_likes = serializers.SerializerMethodField()
    # num_comments = serializers.SerializerMethodField()

    # def get_created_at(self, obj):
    #     dt = timezone.now() - obj.created_at
    #     YEAR_DAYS = 365
    #     MONTH_DAYS = 30
    #     HOUR_SECONDS = 3600
    #     MIN_SECONDS = 60

    #     YEAR = timedelta(days=YEAR_DAYS)
    #     MONTH = timedelta(days=MONTH_DAYS)
    #     DAY = timedelta(days=1)
    #     HOUR = timedelta(seconds=HOUR_SECONDS)
    #     MINUTE = timedelta(seconds=MIN_SECONDS)

    #     if dt >= YEAR:
    #         years = dt.days // YEAR_DAYS
    #         return f"{years}년 전"
    #     elif dt >= MONTH:
    #         months = dt.days // MONTH_DAYS
    #         return f"{months}달 전"
    #     elif dt >= DAY:
    #         days = dt.days
    #         return f"{days}일 전"
    #     elif dt >= HOUR:
    #         hours = dt.seconds // HOUR_SECONDS
    #         return f"{hours}시간 전"
    #     elif dt >= MINUTE:
    #         minutes = dt.seconds // MIN_SECONDS
    #         return f"{minutes}분 전"
    #     else:
    #         return "방금 전"

    def get_is_like(self, feed):
        user = self.context.get('request').user
        #cache => feed.likes.filter(user=user)
        #해당 피드의 좋아요를 눌렀는지 확인
        # 아래처럼 적어줘야 추가 쿼리가 안나간다.
        return len([like for like in feed.likes.all() if like.user==user])

    class Meta:
        model = Feed
        exclude = []
        read_only_fields = [
            "random_nickname"
            ]


class FeedListSerializer(BaseFeedSerializer):

    def create(self, validated_data):
        user = self.context.get('request').user
        random_nickname = default_random_name()
        feed = Feed.objects.create(
            **validated_data,
            random_nickname=random_nickname,
            user=user)
        return feed
