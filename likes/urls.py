
from django.urls import path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .viewsets import FeedLikeViewSet, CommentLikeViewSet


app_name="likes"
router = DefaultRouter()

router.register('feed', FeedLikeViewSet)
router.register('comment', CommentLikeViewSet)

urlpatterns = router.urls
