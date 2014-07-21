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
        u = User.objects.create(authuser=authuser, current_points=0)
        u.save()
        return u

    def has_solved(self, challenge):
        return challenge.solved_by.filter(authuser=self)

    def got_points(self, challenge):
        if challenge.author == self:
            return challenge.solved_by.count() >= 1
        else:
            return self.has_solved(challenge)


class Challenge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    solution = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_author")
    solved_by = models.ManyToManyField(User)
    points = models.IntegerField()

    def check_solution(self, submitted_solution):
        return self.solution.strip() == submitted_solution.strip()

    def user_solved(self, user):
        self.solved_by.add(user)
        user.current_points += self.points
        if self.solved_by.count() == 1:
            # Give points to author
            self.author.current_points += self.points
    
    # Easier debug output
    def __str__(self):
        return self.name

