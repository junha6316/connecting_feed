from django.db.models import Prefetch
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from likes.models import FeedLike, CommentLike

from comments.models import Comment
from comments.serializers import CommentSerializer
from rest_framework.serializers import Serializer

from .serializers import BaseFeedSerializer
from .models import Feed


class CommentListAPIView(ListAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        feed_pk = self.kwargs.get("pk", None)
        feed = get_object_or_404(Feed, pk=feed_pk)

        replies_prefetch: Prefetch = Prefetch(
            "replies", Comment.objects.select_related("user")
        )
        likes_prefetch: Prefetch = Prefetch(
            "likes", CommentLike.objects.select_related("user")
        )

        joined_queryset: QuerySet = queryset.select_related(
            "parent", "feed", "user"
        ).prefetch_related(replies_prefetch, likes_prefetch)
        filtered_queryset: QuerySet = joined_queryset.filter(feed=feed, parent=None)
        return filtered_queryset


class PopularFeedListView(ListAPIView):

    queryset: QuerySet = Feed.objects.select_related("user").prefetch_related(
        Prefetch("likes", queryset=FeedLike.objects.select_related("user"))
    )
    serializer_class: Serializer = BaseFeedSerializer

    def get_queryset(self):
        queryset: QuerySet = super().get_queryset()
        # order를 이 순서대로 먹어야 인덱스 동작
        ordered_qs: QuerySet = queryset.order_by(
            "num_likes", "num_comments", "created_at"
        ).reverse()
        return ordered_qs


class LatestFeedListView(ListAPIView):
    queryset: QuerySet = (
        Feed.objects.select_related("user")
        .prefetch_related(
            Prefetch("likes", queryset=FeedLike.objects.select_related("user"))
        )
        .order_by("-created_at")
    )
    serializer_class = BaseFeedSerializer


class MyFeedListView(ListAPIView):
    queryset = Feed.objects.select_related("user").prefetch_related(
        Prefetch("likes", queryset=FeedLike.objects.select_related("user"))
    )
    serializer_class = BaseFeedSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)
