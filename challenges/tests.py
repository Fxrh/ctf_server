from django.test import TestCase
from django.contrib import auth
from django.core.urlresolvers import reverse

from challenges.models import Challenge, User


class ChallengeModelTest(TestCase):

    def test_simple_creating(self):
        test_user = auth.models.User.objects.create_user(username='Testuser')

        u = User.create_user(test_user)
        self.assertEqual(u.current_points, 0)

        c = Challenge.objects.create(name="Testchallenge", description="test!", solution="1337", points=200, author=u)
        c.save()
        self.assertEqual(c.solved_by.count(), 0)
        self.assertEqual(c.author, u)


class UserModelTest(TestCase):

    def test_from_authuser(self):
        authuser1 = auth.models.User.objects.create_user(username='Testuser1')
        authuser2 = auth.models.User.objects.create_user(username='Testuser2')
        authuser3 = auth.models.User.objects.create_user(username='Testuser3')
        user1 = User.create_user(authuser1)
        user2 = User.create_user(authuser2)
        user3 = User.create_user(authuser3)

        self.assertEqual(user1, User.from_authuser(authuser1))
        self.assertEqual(user3, User.from_authuser(authuser3))
        self.assertNotEqual(user1, User.from_authuser(authuser2))
        self.assertNotEqual(user3, User.from_authuser(authuser2))

    def test_first_user_solves_challenge(self):
        authuser1 = auth.models.User.objects.create_user(username='Testuser1')
        authuser2 = auth.models.User.objects.create_user(username='Testuser2')
        user1 = User.create_user(authuser1)
        user2 = User.create_user(authuser2)

        c = Challenge.objects.create(name="Testchallenge", description="test!", solution="1337", points=200, author=user1)
        c.save()

        self.assertEqual(user1.current_points, 0)
        self.assertEqual(user2.current_points, 0)
        self.assertFalse(user1.has_solved(c))
        self.assertFalse(user2.has_solved(c))
        self.assertFalse(user1.got_points(c))
        self.assertFalse(user2.got_points(c))
        self.assertTrue(user1.is_author(c))
        self.assertFalse(user2.is_author(c))

        self.assertRaises(Exception, c.set_solved, user1)

        c.set_solved(user2)
        self.assertEqual(user1.current_points, 200)
        self.assertEqual(user2.current_points, 200)
        self.assertFalse(user1.has_solved(c))
        self.assertTrue(user2.has_solved(c))
        self.assertTrue(user1.got_points(c))
        self.assertTrue(user2.got_points(c))
        self.assertTrue(user1.is_author(c))
        self.assertFalse(user2.is_author(c))


class IndexViewTest(TestCase):

    def test_index_with_one_challenge(self):
        response = self.client.get(reverse('challenges:index'))
        self.assertEqual(response.status_code, 200)

        test_user = auth.models.User.objects.create_user(username='Testuser')
        u = User.create_user(test_user)
        c = Challenge.objects.create(name="Testchallenge", description="test!", solution="1337", points=200, author=u)
        c.save()
        response = self.client.get(reverse('challenges:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testchallenge")


class InfoViewTest(TestCase):

    def test_info_simple(self):
        test_user = auth.models.User.objects.create_user(username='Testuser')
        u = User.create_user(test_user)
        c = Challenge.objects.create(name="Testchallenge", description="test!", solution="1337", points=200, author=u)
        c.save()

        response = self.client.get(reverse('challenges:info', args=(c.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test!")

        response = self.client.get(reverse('challenges:info', args=(c.id+1,)))
        self.assertEqual(response.status_code, 404)