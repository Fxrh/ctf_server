from django.contrib import admin
from challenges.models import Challenge, User, ChallengeCategory


class UserAdmin(admin.ModelAdmin):
    actions = ['recalculate_points']

    def recalculate_points(self, request, queryset):
        for user in queryset:
            user.recalculate_points()
    recalculate_points.short_description = "Recalculate points"


admin.site.register(Challenge)
admin.site.register(User, UserAdmin)
admin.site.register(ChallengeCategory)

