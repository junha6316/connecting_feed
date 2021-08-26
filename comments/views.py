from rest_framework.generics import CreateAPIView
from .serializers import CommentSerializer


class CommentCreateAPIView(CreateAPIView):

    serializer_class = CommentSerializer
