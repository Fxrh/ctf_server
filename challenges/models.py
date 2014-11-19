from django.db import models
from django.contrib import auth

class User(models.Model):
    authuser = models.ForeignKey(auth.models.User)
    current_points = models.IntegerField()
    ssh_key = models.CharField(max_length=8400)

    @staticmethod
    def from_authuser(authuser):
        return User.objects.get(authuser=authuser)

    @staticmethod
    def create_user(authuser):
        u = User(authuser=authuser, current_points=0)
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


class ChallengeCategory(models.Model):
    name = models.CharField(max_length=200)

    @property
    def challenges(self):
        return Challenge.objects.filter(category=self)


class Challenge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    solution = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_author")
    solved_by = models.ManyToManyField(User)
    points = models.IntegerField()
    category = models.ForeignKey(ChallengeCategory)

    @staticmethod
    def create_challenge( name, solution, author, points, category ):
        c = Challenge( name=name, solution=solution, author=author, points=points, category=category )
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
        if self.solved_by.count() == 1:
            # Give points to author
            self.author.current_points += self.points
    
    # Easier debug output
    def __str__(self):
        return self.name

