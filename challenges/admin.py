from django.contrib import admin
from challenges.models import Challenge, User, ChallengeCategory

admin.site.register(Challenge)
admin.site.register(User)
admin.site.register(ChallengeCategory)

