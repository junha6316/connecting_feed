from rest_framework.routers import DefaultRouter

from .viewsets import FeedViewset
app_name = "feeds"

router = DefaultRouter()
router.register("", FeedViewset)

urlpatterns = router.urls
