from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser



def avatar_directory(instance, filename):
    return f"users/avatar/{instance.pk}/filename"


class User(AbstractUser):

    USER_REGION_CHOICES = (
        ('서울', '서울'),
        ('경기 분당 수원권', '경기 분당 수원권'),
        ('경기 안양 과천권', '경기 안양 과천권'),
        ('경기 알산 파주권', '경기 알산 파주권'),
        ('경기 구리 남양주권', '경기 구리 남양주권'),
        ('경기 의정부권', '경기 의정부권'),
        ('인천', '인천'),
        ('대전', '대전'),
        ('충북', '충북'),
        ('충남', '충남'),
        ('강원', '강원'),
        ('부산', '부산'),
        ('경북', '경북'),
        ('경남', '경남'),
        ('대구', '대구'),
        ('울산', '울산'),
        ('광주', '광주'),
        ('전북', '전북'),
        ('전남', '전남'),
        ('제주', '제주'),
    )

    USER_SEX_CHOICES = (
        ('male', '남성'),
        ('female', '여성'),
        ('etc', '기타'),
    )

    age = models.IntegerField("나이")
    nickname = models.CharField("닉네임", max_length=30)
    sex = models.CharField("성별", choices=USER_SEX_CHOICES, max_length=6)
    region = models.CharField("지역", choices=USER_REGION_CHOICES, max_length=10)
    represent_avatar = models.ImageField(upload_to=avatar_directory)
    indeed_avatar = models.ImageField(upload_to=avatar_directory)
    REQUIRED_FIELDS = ["age"]

    def num_received_likes(self):
        feed_likes = self.feed_likes.all().count()
        comment_likes = self.comment_likes.values('id').count()
        return feed_likes + comment_likes

    def num_received_comments(self):
        num_received_comments = self.comments.all().count()
        return num_received_comments

    class Meta:
        db_table = "users"
