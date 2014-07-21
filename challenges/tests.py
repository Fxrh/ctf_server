from django.test import TestCase
from django.contrib import auth

from challenges.models import Challenge, User


class ChallengeModelTest(TestCase):

    def test_simple_creating(self):
        test_user = auth.models.User.objects.create_user(username='Testuser')

        u = User.create_user(test_user)
        self.assertEqual(u.current_points, 0)

        c = Challenge.objects.create(name="Testchallenge", description="test!", solution="1337", points=200, author=u)
        self.assertEqual(c.solved_by.count(), 0)
        self.assertEqual(c.author, u)
