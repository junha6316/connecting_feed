
from django.urls.conf import path
from rest_framework.routers import DefaultRouter

from .views import MyFeedStatusView

app_name = "users"


router = DefaultRouter()

urlpatterns = [
    path('feed_status/', MyFeedStatusView.as_view(), name="feed_status")
]