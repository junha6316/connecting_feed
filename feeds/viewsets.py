from django.db.models import Prefetch

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from likes.models import FeedLike

from .models import Feed
from .serializers import FeedListSerializer


class FeedViewset(viewsets.ModelViewSet):

    queryset = Feed.objects.select_related("user").prefetch_related(
        Prefetch("likes", queryset=FeedLike.objects.select_related("user"))
    )

    http_method_names = ["post", "head", "options", "trace"]
    serializer_class = FeedListSerializer
    permission_classes = [IsAuthenticated]
