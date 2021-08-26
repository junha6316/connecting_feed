from django.db.models import Count, Prefetch
from django.db.models.query_utils import select_related_descend

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated


from users.models import User
from comments.models import Comment
from likes.models import FeedLike
from .models import Feed
from .serializers import FeedListSerializer


class FeedViewset(viewsets.ModelViewSet):

    queryset = Feed.objects.select_related('user').prefetch_related(
        Prefetch('likes', queryset=FeedLike.objects.select_related('user'))
    )

    http_method_names = [
        'get', 'post', 'put', 'patch', 'head', 'options', 'trace'
        ]
    serializer_class = FeedListSerializer
    permission_classes = [IsAuthenticated]

    # if action == "latest":
    #     return queryset
    # elif action == "popular":
    #     order_criteria = ['num_likes', 'num_comments', 'created_at']
    #     popular_feeds = queryset.order_by(*order_criteria).reverse()
    #     return popular_feeds
    # elif action == "myfeed":
    #     myfeeds = queryset.filter(user=self.request.user)
    #     return myfeeds
    # else:
    #     return queryset
