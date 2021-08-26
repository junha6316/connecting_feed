

from django.urls.conf import path
from rest_framework.routers import DefaultRouter

# from users.viewsets import UserViewSet
from .views import MyFeedStatusView

app_name = "users"


router = DefaultRouter()
# router.register('', UserViewSet)

urlpatterns = [
    path('my-feed-status/', MyFeedStatusView.as_view(), name="feed_status")
]

urlpatterns += router.urls
