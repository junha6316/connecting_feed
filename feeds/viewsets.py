from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Feed
from .serializers import FeedListSerializer


class FeedViewset(viewsets.ModelViewSet):

    queryset = Feed.objects.all()

    http_method_names = ["post", "head", "options", "trace"]
    serializer_class = FeedListSerializer
    permission_classes = [IsAuthenticated]
