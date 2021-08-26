from django.test import TestCase
from django.db import IntegrityError


from likes.models import CommentLike, FeedLike
from comments.models import Comment
from users.models import User
from feeds.models import Feed


class FeedLikeTestCase(TestCase):
    @classmethod
    def create_main_user(self):
        user = User.objects.create(username="test", age=20)
        user.set_password("123")
        user.save()

    @classmethod
    def setUpTestData(cls):
        cls.create_main_user()

    def test_feed_like_create(self):

        user = User.objects.get(username="test")
        feed = Feed.objects.create(body="test", user=user)
        FeedLike.objects.create(user=user, feed=feed)
        self.assertEqual(feed.num_likes, 1)

    def test_feed_like_double_create_on_same_user(self):
        user = User.objects.get(username="test")
        feed = Feed.objects.create(body="test", user=user)
        FeedLike.objects.create(user=user, feed=feed)

        with self.assertRaises(IntegrityError):
            FeedLike.objects.create(user=user, feed=feed)

    def test_feed_like_delete(self):
        user1 = User.objects.get(username="test")
        user2 = User.objects.create(username="abc", password="123", age=20)
        feed = Feed.objects.create(body="test", user=user1)

        FeedLike.objects.create(user=user1, feed=feed)
        FeedLike.objects.create(user=user2, feed=feed)

        # delete feed_like2
        FeedLike.objects.get(user=user2, feed=feed).delete()
        feed = Feed.objects.get(body="test", user=user1)

        self.assertEqual(feed.num_likes, 1)


class CommentikeTestCase(TestCase):
    @classmethod
    def create_main_user(self):
        user = User.objects.create(username="test", age=20)
        user.set_password("123")
        user.save()

    @classmethod
    def setUpTestData(cls):
        cls.create_main_user()

    def test_comment_like_create(self):

        user = User.objects.get(username="test")
        feed = Feed.objects.create(body="test", user=user)
        comment = Comment.objects.create(body="test", feed=feed, user=user)
        CommentLike.objects.create(user=user, comment=comment)
        self.assertEqual(comment.num_likes, 1)

    def test_comment_like_double_create_on_same_user(self):
        user = User.objects.get(username="test")
        feed = Feed.objects.create(body="test", user=user)
        comment = Comment.objects.create(body="test", feed=feed, user=user)
        CommentLike.objects.create(user=user, comment=comment)

        with self.assertRaises(IntegrityError):
            CommentLike.objects.create(user=user, comment=comment)

    def test_feed_like_delete(self):
        user1 = User.objects.get(username="test")
        user2 = User.objects.create(username="abc", password="123", age=20)
        feed = Feed.objects.create(body="test", user=user1)
        comment = Comment.objects.create(body="test", feed=feed, user=user1)

        CommentLike.objects.create(user=user1, comment=comment)
        CommentLike.objects.create(user=user2, comment=comment)

        # delete feed_like2
        CommentLike.objects.get(user=user2, comment=comment).delete()
        comment = Comment.objects.get(body="test", feed=feed, user=user1)

        self.assertEqual(comment.num_likes, 1)
