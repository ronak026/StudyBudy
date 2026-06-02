"""Tests for the base app: models, auth/room views, and the REST API."""

from django.test import TestCase
from django.urls import reverse

from .models import User, Topic, Room, Message


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice", email="alice@example.com", password="pass12345"
        )
        self.topic = Topic.objects.create(name="Python")
        self.room = Room.objects.create(
            host=self.user, topic=self.topic, name="Django study", description="Learn Django"
        )

    def test_room_str(self):
        self.assertEqual(str(self.room), "Django study")

    def test_topic_str(self):
        self.assertEqual(str(self.topic), "Python")

    def test_message_str_truncates_to_50_chars(self):
        body = "x" * 80
        msg = Message.objects.create(user=self.user, room=self.room, body=body)
        self.assertEqual(str(msg), "x" * 50)

    def test_room_default_ordering_newest_first(self):
        second = Room.objects.create(host=self.user, topic=self.topic, name="Second")
        self.assertEqual(list(Room.objects.all())[0], second)

    def test_email_is_the_username_field(self):
        self.assertEqual(User.USERNAME_FIELD, "email")


class AuthViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bob", email="bob@example.com", password="pass12345"
        )

    def test_login_page_renders(self):
        res = self.client.get(reverse("login"))
        self.assertEqual(res.status_code, 200)

    def test_login_with_valid_credentials_redirects_home(self):
        res = self.client.post(
            reverse("login"), {"email": "bob@example.com", "password": "pass12345"}
        )
        self.assertRedirects(res, reverse("home"))

    def test_login_with_unknown_email_does_not_crash(self):
        res = self.client.post(
            reverse("login"), {"email": "nobody@example.com", "password": "x"}
        )
        self.assertEqual(res.status_code, 200)  # stays on the login page, no 500

    def test_register_creates_user_and_lowercases_username(self):
        res = self.client.post(
            reverse("register"),
            {
                "name": "Carol",
                "username": "CAROL",
                "email": "carol@example.com",
                "password1": "Str0ngPass!23",
                "password2": "Str0ngPass!23",
            },
        )
        self.assertRedirects(res, reverse("login"))
        self.assertTrue(User.objects.filter(username="carol").exists())


class RoomViewTests(TestCase):
    def setUp(self):
        self.host = User.objects.create_user(
            username="host", email="host@example.com", password="pass12345"
        )
        self.topic = Topic.objects.create(name="Math")
        self.room = Room.objects.create(host=self.host, topic=self.topic, name="Calculus")

    def test_home_renders(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)

    def test_home_search_matches_partial_name(self):
        res = self.client.get(reverse("home"), {"q": "calc"})
        self.assertContains(res, "Calculus")

    def test_room_page_renders(self):
        res = self.client.get(reverse("room", args=[self.room.id]))
        self.assertEqual(res.status_code, 200)

    def test_room_missing_id_returns_404(self):
        res = self.client.get(reverse("room", args=[9999]))
        self.assertEqual(res.status_code, 404)

    def test_posting_message_requires_login(self):
        res = self.client.post(
            reverse("room", args=[self.room.id]), {"body": "hi"}, follow=True
        )
        self.assertEqual(Message.objects.count(), 0)

    def test_logged_in_user_can_post_message_and_join(self):
        self.client.force_login(self.host)
        self.client.post(reverse("room", args=[self.room.id]), {"body": "first post"})
        self.assertEqual(Message.objects.count(), 1)
        self.assertIn(self.host, self.room.participants.all())

    def test_create_room_requires_login(self):
        res = self.client.get(reverse("create-room"))
        self.assertEqual(res.status_code, 302)  # redirected to login

    def test_non_host_cannot_delete_room(self):
        other = User.objects.create_user(
            username="other", email="other@example.com", password="pass12345"
        )
        self.client.force_login(other)
        res = self.client.post(reverse("delete-room", args=[self.room.id]))
        self.assertEqual(res.status_code, 200)  # "not allowed" response, not a delete
        self.assertTrue(Room.objects.filter(id=self.room.id).exists())


class ApiTests(TestCase):
    def setUp(self):
        self.host = User.objects.create_user(
            username="api", email="api@example.com", password="pass12345"
        )
        self.topic = Topic.objects.create(name="Science")
        self.room = Room.objects.create(host=self.host, topic=self.topic, name="Physics")

    def test_get_rooms_returns_list(self):
        res = self.client.get("/api/rooms/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)

    def test_get_single_room(self):
        res = self.client.get(f"/api/rooms/{self.room.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["name"], "Physics")

    def test_get_missing_room_returns_404(self):
        res = self.client.get("/api/rooms/9999/")
        self.assertEqual(res.status_code, 404)
