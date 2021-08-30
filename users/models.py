from typing import Any

from django.db import models
from django.db.models import QuerySet
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser


def avatar_directory(instance, filename):
    return f"users/avatar/{instance.pk}/filename"


class MyModelManger(models.Manager):

    region_dic = {
        "서울": 0,
        "경기 분당 수원권": 1,
        "경기 안양 과천권": 2,
        "경기 일산 파주권": 3,
        "경기 구리 남양주권": 4,
        "경기 의정부권": 5,
        "인천": 6,
        "대전": 7,
        "충북": 8,
        "충남": 9,
        "강원": 10,
        "부산": 11,
        "경북": 12,
        "경남": 13,
        "대구": 14,
        "울산": 15,
        "광주": 16,
        "전북": 17,
        "전남": 18,
        "제주": 19,
    }

    def filter(self, *args: Any, **kwargs: Any) -> QuerySet[Any]:
        region = kwargs.get("region", None)
        if region:
            region_id = self.region_dic[region]
            kwargs["region"] = region_id
            return super().filter(*args, **kwargs)
        return super().filter(*args, **kwargs)


class User(AbstractUser):

    USER_REGION_CHOICES = (
        (0, "서울"),
        (1, "경기 분당 수원권"),
        (2, "경기 안양 과천권"),
        (3, "경기 일산 파주권"),
        (4, "경기 구리 남양주권"),
        (5, "경기 의정부권"),
        (6, "인천"),
        (7, "대전"),
        (8, "충북"),
        (9, "충남"),
        (10, "강원"),
        (11, "부산"),
        (12, "경북"),
        (13, "경남"),
        (14, "대구"),
        (15, "울산"),
        (16, "광주"),
        (17, "전북"),
        (18, "전남"),
        (19, "제주"),
    )

    USER_SEX_CHOICES = (
        (1, "남성"),
        (2, "여성"),
        (3, "기타"),
    )
    # 수정: 필드의 특성 고려해서 models.field 사용
    age = models.IntegerField("나이")
    nickname = models.CharField("닉네임", max_length=30)
    sex = models.CharField("성별", choices=USER_SEX_CHOICES, max_length=6)
    region = models.CharField("지역", choices=USER_REGION_CHOICES, max_length=10)
    represent_avatar = models.ImageField(upload_to=avatar_directory)
    indeed_avatar = models.ImageField(upload_to=avatar_directory)
    objects = MyModelManger()
    REQUIRED_FIELDS = ["age"]

    def num_received_feed_likes(self):
        feedlike_qs = self.feeds.values("num_likes").cache()
        total_feedlikes_num = feedlike_qs.aggregate(total_likes=Sum("num_likes"))
        return total_feedlikes_num["total_likes"]

    def num_received_comments(self):
        comments_qs = self.feeds.values("num_comments").cache()
        total_comments_num = comments_qs.aggregate(total_comments=Sum("num_comments"))
        return total_comments_num["total_comments"]

    class Meta:
        db_table = "users"
