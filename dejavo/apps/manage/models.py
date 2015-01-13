from django.db import models
from django.conf import settings

class Complain(models.Model):
    
   COMPLAIN_TYPE = (
           ('qanda', 'QandA'),
           ('article', 'Article'),
           ('message', 'Message'),
           ('notice', 'Notice'),
           ('etc', 'Etc'),
    )

   complain_type = models.CharField(max_length = 10, choices = COMPLAIN_TYPE)
   sender = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            related_name = 'complain_report')
   meta = models.TextField() # json
   content = models.TextField()
   created_date = models.DateTimeField(auto_now_add = True)

class Log(models.Model):

    LOG_TYPE = (
        ('login', 'LOGIN'),
        ('logout', 'LOGOUT'),
    )

    log_type = models.CharField(max_length = 10, choices = LOG_TYPE)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL)
    action_date = models.DateTimeField(auto_now_add = True)
    meta = models.TextField() # to have additional information
