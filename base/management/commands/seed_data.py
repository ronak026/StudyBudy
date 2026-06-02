"""Seed the database with sample users, topics, rooms, and messages.

Usage:
    python manage.py seed_data            # 50 rooms (default)
    python manage.py seed_data --rooms 30
    python manage.py seed_data --flush    # delete existing rooms/messages/topics first
"""

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from base.models import User, Topic, Room, Message

TOPICS = [
    "Python", "Django", "JavaScript", "React", "Machine Learning",
    "Data Science", "Algorithms", "System Design", "DevOps", "Databases",
    "Web Development", "Mobile Apps", "Cybersecurity", "Cloud Computing", "UI/UX",
]

USERS = [
    ("alice", "Alice Johnson"), ("bob", "Bob Smith"), ("carol", "Carol Lee"),
    ("dave", "Dave Patel"), ("erin", "Erin Garcia"), ("frank", "Frank Müller"),
    ("grace", "Grace Kim"), ("henry", "Henry Adams"), ("isabel", "Isabel Rossi"),
    ("jack", "Jack Nguyen"),
]

ROOM_TEMPLATES = [
    "Let's learn {topic} together",
    "{topic} study group",
    "Beginners diving into {topic}",
    "Advanced {topic} discussion",
    "Daily {topic} practice",
    "{topic} interview prep",
    "Building projects with {topic}",
    "{topic} doubts and Q&A",
    "Weekend {topic} bootcamp",
    "Mastering {topic} fundamentals",
]

DESCRIPTIONS = [
    "Share resources, ask questions, and learn together.",
    "A friendly space for learners of all levels.",
    "We meet to solve problems and review concepts.",
    "Bring your doubts — no question is too small.",
    "Project-based learning with weekly goals.",
    "Prepping for interviews and coding challenges.",
]

MESSAGES = [
    "Hey everyone, excited to join!",
    "Can someone explain this concept?",
    "Here's a great resource I found.",
    "Anyone up for a study session tonight?",
    "I finally solved that problem 🎉",
    "What are you all working on this week?",
    "Thanks, that really helped!",
    "Let's schedule a call to discuss.",
    "Just shared my notes in the description.",
    "Great progress everyone, keep it up!",
]


class Command(BaseCommand):
    help = "Seed the database with sample users, topics, rooms, and messages."

    def add_arguments(self, parser):
        parser.add_argument("--rooms", type=int, default=50, help="Number of rooms to create.")
        parser.add_argument("--flush", action="store_true", help="Delete existing rooms/messages/topics first.")

    @transaction.atomic
    def handle(self, *args, **options):
        rng = random.Random(42)  # reproducible

        if options["flush"]:
            Message.objects.all().delete()
            Room.objects.all().delete()
            Topic.objects.all().delete()
            self.stdout.write(self.style.WARNING("Flushed existing rooms, messages, and topics."))

        users = []
        for username, name in USERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"name": name, "email": f"{username}@example.com"},
            )
            if created:
                user.set_password("password123")
                user.save()
            users.append(user)

        topics = [Topic.objects.get_or_create(name=t)[0] for t in TOPICS]

        now = timezone.now()
        rooms_created = 0
        messages_created = 0
        for _ in range(options["rooms"]):
            topic = rng.choice(topics)
            host = rng.choice(users)
            name = rng.choice(ROOM_TEMPLATES).format(topic=topic.name)
            room = Room.objects.create(
                host=host,
                topic=topic,
                name=name,
                description=rng.choice(DESCRIPTIONS),
            )
            rooms_created += 1

            # Spread creation times across the last ~30 days (auto_now fields
            # must be overridden with an update() to take effect).
            created_at = now - timedelta(
                days=rng.randint(0, 30), hours=rng.randint(0, 23), minutes=rng.randint(0, 59)
            )
            Room.objects.filter(pk=room.pk).update(created=created_at, updated=created_at)

            participants = rng.sample(users, rng.randint(2, 6))
            room.participants.add(*participants)

            last = created_at
            for _ in range(rng.randint(1, 5)):
                msg = Message.objects.create(
                    user=rng.choice(participants),
                    room=room,
                    body=rng.choice(MESSAGES),
                )
                # Each reply lands a bit after the previous one, up to now.
                last = min(last + timedelta(hours=rng.randint(1, 48)), now)
                Message.objects.filter(pk=msg.pk).update(created=last, updated=last)
                messages_created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(users)} users, {len(topics)} topics, "
            f"{rooms_created} rooms, {messages_created} messages."
        ))
        self.stdout.write("Sample login: alice@example.com / password123")
