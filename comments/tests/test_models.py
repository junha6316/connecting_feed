from comments.models import Comment
from django.test import TestCase

from users.models import User
from feeds.models import Feed


class CommentModelTestCase(TestCase):
    @classmethod
    def create_main_user(self):
        user = User.objects.create(username="test", age=20)
        user.set_password("123")
        user.save()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.create_main_user()

    def test_num_comments_signal_on_create(self):
        user = User.objects.get(username="test")
        feed = Feed.objects.create(user=user, body="test")
        Comment.objects.create(feed=feed, user=user)
        feed = Feed.objects.get(user=user, body="test")
        self.assertEqual(feed.num_comments, 1)

    def test_num_comments_signal_on_delete(self):
        user = User.objects.get(username="test")
        feed = Feed.objects.create(user=user, body="test")

        Comment.objects.create(feed=feed, body="comment1", user=user)
        Comment.objects.create(feed=feed, body="comment2", user=user)

        Comment.objects.get(feed=feed, user=user, body="comment2").delete()
        feed = Feed.objects.get(user=user, body="test")
        self.assertEqual(feed.num_comments, 1)
