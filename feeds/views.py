

from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView

from likes.models import FeedLike, CommentLike

from comments.models import Comment
from comments.serializers import CommentSerializer

from .serializers import BaseFeedSerializer
from .models import Feed


class CommentListAPIView(ListAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        feed_pk = self.kwargs.get('pk', None)

        filtered_queryset = queryset.select_related(
                            'parent', 'feed', 'user'
                            ).prefetch_related(
                                Prefetch(
                                    'replies', Comment.objects.select_related('user')
                                    ),
                                Prefetch(
                                    'likes', CommentLike.objects.select_related('user')
                                    )
                                ).filter(feed=feed_pk, parent=None)
        return filtered_queryset


class PopularFeedListView(ListAPIView):

    queryset = Feed.objects.select_related('user').prefetch_related(
        Prefetch('likes', queryset=FeedLike.objects.select_related('user'))
    )
    serializer_class = BaseFeedSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # order를 이 순서대로 먹어야 인덱스 동작
        result = queryset.order_by('num_likes', 'num_comments', 'created_at').reverse()
        return result


class LatestFeedListView(ListAPIView):
    queryset = Feed.objects.select_related('user').prefetch_related(
        Prefetch('likes', queryset=FeedLike.objects.select_related('user'))
    ).order_by('-created_at')
    serializer_class = BaseFeedSerializer


class MyFeedListView(ListAPIView):
    queryset = Feed.objects.select_related('user').prefetch_related(
        Prefetch('likes', queryset=FeedLike.objects.select_related('user'))
    )
    serializer_class = BaseFeedSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)




