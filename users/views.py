from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .serializers import MyActivitySerializer


class MyFeedStatusView(APIView):

    premission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            status=HTTP_200_OK,
            data=MyActivitySerializer(request.user).data
            )
