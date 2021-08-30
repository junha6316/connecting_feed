from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser


def avatar_directory(instance, filename):
    return f"users/avatar/{instance.pk}/filename"


class User(AbstractUser):

    USER_REGION_CHOICES = (
        ("서울", "서울"),
        ("경기 분당 수원권", "경기 분당 수원권"),
        ("경기 안양 과천권", "경기 안양 과천권"),
        ("경기 알산 파주권", "경기 알산 파주권"),
        ("경기 구리 남양주권", "경기 구리 남양주권"),
        ("경기 의정부권", "경기 의정부권"),
        ("인천", "인천"),
        ("대전", "대전"),
        ("충북", "충북"),
        ("충남", "충남"),
        ("강원", "강원"),
        ("부산", "부산"),
        ("경북", "경북"),
        ("경남", "경남"),
        ("대구", "대구"),
        ("울산", "울산"),
        ("광주", "광주"),
        ("전북", "전북"),
        ("전남", "전남"),
        ("제주", "제주"),
    )

    USER_SEX_CHOICES = (
        ("male", "남성"),
        ("female", "여성"),
        ("etc", "기타"),
    )
    # 수정: 필드의 특성 고려해서 models.field 사용
    age = models.IntegerField("나이")
    nickname = models.CharField("닉네임", max_length=30)
    sex = models.CharField("성별", choices=USER_SEX_CHOICES, max_length=6)
    region = models.CharField("지역", choices=USER_REGION_CHOICES, max_length=10)
    represent_avatar = models.ImageField(upload_to=avatar_directory)
    indeed_avatar = models.ImageField(upload_to=avatar_directory)
    # num_received_likes = models.IntegerField()
    # num_received_comments = models.IntegerField()
    # num_feeds = models.IntegerField()
    # num_comments = models.IntegerField()
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
