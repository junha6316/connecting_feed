from django.urls.conf import path

from rest_framework.routers import DefaultRouter

from .viewsets import FeedViewset
from .views import (
    CommentListAPIView,
    LatestFeedListView,
    MyFeedListView,
    PopularFeedListView,
)


app_name = "feeds"

router = DefaultRouter()
router.register("", FeedViewset)


urlpatterns = [
    path("latest/", LatestFeedListView.as_view(), name="latest"),
    path("popular/", PopularFeedListView.as_view(), name="popular"),
    path("myfeed/", MyFeedListView.as_view(), name="myfeed"),
    path("<int:pk>/comments/", CommentListAPIView.as_view(), name="comments"),
] + router.urls
