from django.db.models import Prefetch
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView

from comments.models import Comment
from comments.serializers import CommentSerializer
from .serializers import BaseFeedSerializer
from .models import Feed


class CommentListAPIView(ListAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        feed_pk = self.kwargs.get("pk", None)
        feed = get_object_or_404(Feed, pk=feed_pk)
        replies_qs: Prefetch = Prefetch(
            "replies",
            Comment.objects.select_related(
                "user", "root", "parent", "feed"
            ).prefetch_related("likes__user"),
        )
        comment_likes_qs: str = "likes__user"

        joined_queryset: QuerySet = queryset.select_related(
            "feed", "root", "user"
        ).prefetch_related(comment_likes_qs, replies_qs)

        filtered_queryset: QuerySet = joined_queryset.filter(
            feed=feed, root=None
        ).cache()
        return filtered_queryset


class BaseFeedListView(ListAPIView):

    queryset = Feed.objects.select_related("user").prefetch_related("likes__user")
    serializer_class = BaseFeedSerializer


class PopularFeedListView(BaseFeedListView):
    def get_queryset(self):
        queryset: QuerySet = super().get_queryset()
        # order를 이 순서대로 먹어야 인덱스 동작
        # 수정: -num_likes로 인덱싱 걸기
        ordered_qs: QuerySet = (
            queryset.order_by("num_likes", "num_comments", "created_at")
            .reverse()
            .cache()
        )
        return ordered_qs


class LatestFeedListView(BaseFeedListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        ordered_qs = queryset.order_by("-created_at").cache()
        return ordered_qs


class MyFeedListView(BaseFeedListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user).cache()
