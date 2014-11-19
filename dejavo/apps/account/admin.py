from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import User
from django.contrib.auth.admin import UserAdmin
from dejavo.apps.account.models import UserProfile, Club

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

class ClubAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Club, ClubAdmin)
