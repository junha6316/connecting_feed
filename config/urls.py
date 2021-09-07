"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from rest_framework.permissions import IsAuthenticated

import debug_toolbar

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Connecting Feed API",
        default_version="v1",
        description="Connecting 피드 API 문서",
    ),
    public=True,
    permission_classes=[IsAuthenticated],
)

# versioning은 앱마다 하고 있음
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/feeds/", include("feeds.urls", namespace="feeds")),
    path("api/v1/comments/", include("comments.urls", namespace="comments")),
    path("api/v1/likes/", include("likes.urls", namespace="likes")),
    path("api/v1/users/", include("users.urls", namespace="users")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("__debug__/", include(debug_toolbar.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        )
    ]
