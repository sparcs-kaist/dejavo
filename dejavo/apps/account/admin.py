from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from dejavo.apps.account.models import UserProfile, Notification

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class NotificationAdmin(admin.ModelAdmin):
    model = Notification

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Notification, NotificationAdmin)
