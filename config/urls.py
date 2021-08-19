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
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/feeds/', include('feeds.urls', namespace="feeds")),
    path('api/v1/comments/', include('comments.urls', namespace="comments")),
    path('api/v1/replies/', include('replies.urls', namespace="replies")),
    path('api/v1/likes/', include('likes.urls', namespace="likes")),
    path("api-auth/", include('rest_framework.urls', namespace="rest_framework")),
    
]
