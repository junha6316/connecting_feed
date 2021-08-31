from django.urls import path

from .views import token, refresh_token

app_name = "users"

urlpatterns = [
    path("token/", token, name="token"),
    path("token/refresh/", refresh_token, name="refresh_token"),
]
