from django.db import models
from django.contrib import auth

class User(models.Model):
    authuser = models.ForeignKey(auth.models.User)
    current_points = models.IntegerField()
    ssh_key = models.CharField(max_length=8400, blank=True)
    allow_create = models.BooleanField(default=False)

    @staticmethod
    def from_authuser(authuser):
        return User.objects.get(authuser=authuser)

    @staticmethod
    def create_user(authuser):
        u = User(authuser=authuser, current_points=0, allow_create=False)
        u.save()
        return u

    def has_solved(self, challenge):
        return challenge.solved_by.filter(authuser=self).exists()

    def got_points(self, challenge):
        if challenge.author == self:
            return challenge.solved_by.count() >= 1
        else:
            return self.has_solved(challenge)

    def is_author(self, challenge):
        return challenge.author == self

    @staticmethod
    def getRanking():
        return User.objects.order_by('-current_points') # - == descending

    def __str__(self):
        return self.authuser.get_username()


class ChallengeCategory(models.Model):
    name = models.CharField(max_length=200)

    @property
    def challenges(self):
        return Challenge.objects.filter(category=self, is_published=True)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    name = models.CharField(max_length=40, verbose_name='name')
    description = models.TextField(verbose_name="description")
    solution = models.CharField(max_length=200, verbose_name='solution')
    author = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_author", verbose_name='author')
    solved_by = models.ManyToManyField(User, verbose_name='solved by')
    points = models.IntegerField(verbose_name='points')
    category = models.ForeignKey(ChallengeCategory, verbose_name='category')
    is_published = models.BooleanField(verbose_name='is published', default=False)

    @staticmethod
    def create_challenge( name, solution, author, points, category ):
        c = Challenge( name=name, solution=solution, author=author, points=points, category=category,
                       is_published=False )
        c.save()
        return c

    @staticmethod
    def does_name_exist( name ):
        return Challenge.objects.filter(name=name).exists()

    def check_solution(self, submitted_solution):
        return self.solution.strip() == submitted_solution.strip()

    def set_solved(self, user):
        if user == self.author:
            raise Exception("Author can't solve his own challenge")
        self.solved_by.add(user)
        user.current_points += self.points
        user.save()
        if self.solved_by.count() == 1:
            # Give points to author
            self.author.current_points += self.points
            self.author.save()
    
    # Easier debug output
    def __str__(self):
        return self.name

