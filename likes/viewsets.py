
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import FeedLikeSerializer, CommentLikeSerializer
from .models import FeedLike, CommentLike


class FeedLikeViewSet(ModelViewSet):
    queryset = FeedLike.objects.all()
    http_method_names = ['post', 'delete', 'head', 'options', 'trace']
    serializer_class = FeedLikeSerializer
    permission_classes = [IsAuthenticated]


class CommentLikeViewSet(ModelViewSet):
    queryset = CommentLike.objects.all()
    http_method_names = ['post', 'delete', 'head', 'options', 'trace']
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]
