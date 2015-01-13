from django.contrib import admin
from dejavo.apps.manage.models import Complain, Log

class ComplainAdmin(admin.ModelAdmin):
    model = Complain

class LogAdmin(admin.ModelAdmin):
    model = Log

admin.site.register(Complain, ComplainAdmin)
admin.site.register(Log, LogAdmin)
