from django.contrib import admin

from .models import Feed


@admin.register(Feed)
class FeedModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'random_nickname',
        'body',
        'num_likes',
        'num_comments',
    )