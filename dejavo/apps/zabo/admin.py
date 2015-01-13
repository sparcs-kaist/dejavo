from django.contrib import admin
from dejavo.apps.zabo.models import Article, Poster, Announcement, \
        Question, Answer

class ArticleAdmin(admin.ModelAdmin):
    model = Article

class PosterAdmin(admin.ModelAdmin):
    model = Poster

class AnnouncementAdmin(admin.ModelAdmin):
    model = Announcement

class QuestionAdmin(admin.ModelAdmin):
    model = Question

class AnswerAdmin(admin.ModelAdmin):
    model = Answer

admin.site.register(Article, ArticleAdmin)
admin.site.register(Poster, PosterAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
