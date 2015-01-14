from django.contrib import admin
from dejavo.apps.zabo.models import Article, Poster, Announcement, \
        Question, Answer, Attachment, Timeslot, Contact

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1

class PosterInline(admin.TabularInline):
    model = Poster
    extra = 1

class TimeslotInline(admin.StackedInline):
    model = Timeslot
    extra = 1

class AttachmentInline(admin.StackedInline):
    model = Attachment
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    inlines = [ContactInline, PosterInline, AttachmentInline, TimeslotInline]

class AnnouncementAdmin(admin.ModelAdmin):
    model = Announcement

class QuestionAdmin(admin.ModelAdmin):
    model = Question

class AnswerAdmin(admin.ModelAdmin):
    model = Answer

admin.site.register(Article, ArticleAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
