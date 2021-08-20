from django.db.models import Count

from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated

from .models import Feed
from .serializers import FeedListSerializer


class FeedViewset(viewsets.ModelViewSet):

    queryset = Feed.objects.prefetch_related('feed_likes', 'comments')
    http_method_names = [
        'get', 'post', 'put', 'patch', 'head', 'options', 'trace'
        ]
    serializer_class = FeedListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get("category", None)

        if category == "latest":
            return queryset
        elif category == "popular":
            order_criteria = ['num_likes', 'num_comments']
            feeds = queryset.annotate(
                num_likes=Count("feed_likes"),
                num_comments=Count("comments")
                )
            popular_feeds = feeds.order_by(*order_criteria)
            return popular_feeds
        elif category == "myfeed":
            myfeeds = queryset.filter(user=self.request.user)
            return myfeeds
        else:
            #명확하게 제공해야할거 같은데;
            return queryset
